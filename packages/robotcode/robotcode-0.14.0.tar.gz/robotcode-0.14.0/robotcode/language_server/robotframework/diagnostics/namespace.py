from __future__ import annotations

import ast
import asyncio
import enum
import itertools
import logging
import time
import weakref
from collections import OrderedDict
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

from ....utils.async_itertools import as_async_iterable
from ....utils.async_tools import Lock, async_event
from ....utils.logging import LoggingDescriptor
from ....utils.uri import Uri
from ...common.lsp_types import (
    CodeDescription,
    Diagnostic,
    DiagnosticRelatedInformation,
    DiagnosticSeverity,
    DiagnosticTag,
    DocumentUri,
    Location,
    Position,
    Range,
)
from ...common.text_document import TextDocument
from ..languages import Languages
from ..utils.ast_utils import (
    Token,
    range_from_node,
    range_from_token,
    strip_variable_token,
    tokenize_variables,
)
from ..utils.async_ast import AsyncVisitor
from ..utils.match import eq
from ..utils.variables import BUILTIN_VARIABLES
from ..utils.version import get_robot_version
from .entities import (
    ArgumentDefinition,
    BuiltInVariableDefinition,
    CommandLineVariableDefinition,
    EnvironmentVariableDefinition,
    Import,
    InvalidVariableError,
    LibraryImport,
    LocalVariableDefinition,
    ResourceImport,
    VariableDefinition,
    VariableMatcher,
    VariablesImport,
)
from .imports_manager import ImportsManager
from .library_doc import (
    BUILTIN_LIBRARY_NAME,
    DEFAULT_LIBRARIES,
    KeywordDoc,
    KeywordError,
    KeywordMatcher,
    LibraryDoc,
)

DIAGNOSTICS_SOURCE_NAME = "robotcode.namespace"


class DiagnosticsError(Exception):
    pass


class DiagnosticsWarningError(DiagnosticsError):
    pass


class ImportError(DiagnosticsError):
    pass


class NameSpaceError(Exception):
    pass


class VariablesVisitor(AsyncVisitor):
    async def get(self, source: str, model: ast.AST) -> List[VariableDefinition]:
        self._results: List[VariableDefinition] = []
        self.source = source
        await self.visit(model)
        return self._results

    async def visit_Section(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.model.blocks import VariableSection

        if isinstance(node, VariableSection):
            await self.generic_visit(node)

    async def visit_Variable(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import Variable
        from robot.variables import search_variable

        variable = cast(Variable, node)

        name_token = variable.get_token(RobotToken.VARIABLE)
        name = name_token.value

        if name is not None:

            match = search_variable(name, ignore_errors=True)
            if not match.is_assign(allow_assign_mark=True):
                return

            if name.endswith("="):
                name = name[:-1].rstrip()

            has_value = bool(variable.value)
            value = tuple(
                s.replace("${CURDIR}", str(Path(self.source).parent).replace("\\", "\\\\")) for s in variable.value
            )

            self._results.append(
                VariableDefinition(
                    name=variable.name,
                    name_token=strip_variable_token(
                        RobotToken(name_token.type, name, name_token.lineno, name_token.col_offset, name_token.error)
                    ),
                    line_no=variable.lineno,
                    col_offset=variable.col_offset,
                    end_line_no=variable.lineno,
                    end_col_offset=variable.end_col_offset,
                    source=self.source,
                    has_value=has_value,
                    resolvable=True,
                    value=value,
                )
            )


class BlockVariableVisitor(AsyncVisitor):
    def __init__(
        self, namespace: Namespace, source: str, position: Optional[Position] = None, in_args: bool = True
    ) -> None:
        super().__init__()
        self.namespace = namespace
        self.source = source
        self.position = position
        self.in_args = in_args

        self._results: Dict[str, VariableDefinition] = {}
        self.current_kw_doc: Optional[KeywordDoc] = None

    async def get(self, model: ast.AST) -> List[VariableDefinition]:

        self._results = {}

        await self.visit(model)

        return list(self._results.values())

    async def visit(self, node: ast.AST) -> None:
        if self.position is None or self.position >= range_from_node(node).start:
            return await super().visit(node)

    async def visit_Keyword(self, node: ast.AST) -> None:  # noqa: N802
        try:
            await self.generic_visit(node)
        finally:
            self.current_kw_doc = None

    async def visit_KeywordName(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import KeywordName
        from robot.variables.search import search_variable

        from ..parts.model_helper import ModelHelperMixin

        n = cast(KeywordName, node)
        name_token = cast(Token, n.get_token(RobotToken.KEYWORD_NAME))

        if name_token is not None and name_token.value:
            keyword = await ModelHelperMixin.get_keyword_definition_at_token(self.namespace, name_token)
            self.current_kw_doc = keyword

            for variable_token in filter(
                lambda e: e.type == RobotToken.VARIABLE,
                tokenize_variables(name_token, identifiers="$", ignore_errors=True),
            ):
                if variable_token.value:

                    match = search_variable(variable_token.value, "$", ignore_errors=True)
                    if match.base is None:
                        continue
                    name = match.base.split(":", 1)[0]
                    full_name = f"{match.identifier}{{{name}}}"
                    var_token = strip_variable_token(variable_token)
                    var_token.value = name
                    self._results[full_name] = ArgumentDefinition(
                        name=full_name,
                        name_token=var_token,
                        line_no=variable_token.lineno,
                        col_offset=variable_token.col_offset,
                        end_line_no=variable_token.lineno,
                        end_col_offset=variable_token.end_col_offset,
                        source=self.source,
                        keyword_doc=self.current_kw_doc,
                    )

    def get_variable_token(self, token: Token) -> Optional[Token]:
        from robot.parsing.lexer.tokens import Token as RobotToken

        return next(
            (
                v
                for v in itertools.dropwhile(
                    lambda t: t.type in RobotToken.NON_DATA_TOKENS,
                    tokenize_variables(token, ignore_errors=True),
                )
                if v.type == RobotToken.VARIABLE
            ),
            None,
        )

    async def visit_Arguments(self, node: ast.AST) -> None:  # noqa: N802
        from robot.errors import VariableError
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import Arguments

        args: List[str] = []
        n = cast(Arguments, node)
        arguments = n.get_tokens(RobotToken.ARGUMENT)
        argument_definitions = []

        for argument_token in (cast(RobotToken, e) for e in arguments):
            try:
                argument = self.get_variable_token(argument_token)

                if argument is not None and argument.value != "@{}":
                    if (
                        self.in_args
                        and self.position is not None
                        and self.position in range_from_token(argument_token)
                        and self.position > range_from_token(argument).end
                    ):
                        break

                    if argument.value not in args:
                        args.append(argument.value)
                        arg_def = ArgumentDefinition(
                            name=argument.value,
                            name_token=strip_variable_token(argument),
                            line_no=argument.lineno,
                            col_offset=argument.col_offset,
                            end_line_no=argument.lineno,
                            end_col_offset=argument.end_col_offset,
                            source=self.source,
                            keyword_doc=self.current_kw_doc,
                        )
                        self._results[argument.value] = arg_def
                        argument_definitions.append(arg_def)

            except VariableError:
                pass

        if self.current_kw_doc is not None:
            self.current_kw_doc.argument_definitions = argument_definitions

    async def visit_ExceptHeader(self, node: ast.AST) -> None:  # noqa: N802
        from robot.errors import VariableError
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import ExceptHeader
        from robot.variables import is_scalar_assign

        n = cast(ExceptHeader, node)
        variables = n.get_tokens(RobotToken.VARIABLE)[:1]
        if variables and is_scalar_assign(variables[0].value):
            try:
                variable = self.get_variable_token(variables[0])

                if variable is not None:
                    self._results[variable.value] = LocalVariableDefinition(
                        name=variable.value,
                        name_token=strip_variable_token(variable),
                        line_no=variable.lineno,
                        col_offset=variable.col_offset,
                        end_line_no=variable.lineno,
                        end_col_offset=variable.end_col_offset,
                        source=self.source,
                    )

            except VariableError:
                pass

    async def visit_KeywordCall(self, node: ast.AST) -> None:  # noqa: N802
        from robot.errors import VariableError
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import KeywordCall

        # TODO  analyze "Set Local/Global/Suite Variable"

        n = cast(KeywordCall, node)

        for assign_token in n.get_tokens(RobotToken.ASSIGN):
            variable_token = self.get_variable_token(assign_token)

            try:
                if variable_token is not None:
                    if (
                        self.position is not None
                        and self.position in range_from_node(n)
                        and self.position > range_from_token(variable_token).end
                    ):
                        continue

                    if variable_token.value not in self._results:
                        self._results[variable_token.value] = LocalVariableDefinition(
                            name=variable_token.value,
                            name_token=strip_variable_token(variable_token),
                            line_no=variable_token.lineno,
                            col_offset=variable_token.col_offset,
                            end_line_no=variable_token.lineno,
                            end_col_offset=variable_token.end_col_offset,
                            source=self.source,
                        )

            except VariableError:
                pass

    async def visit_InlineIfHeader(self, node: ast.AST) -> None:  # noqa: N802
        from robot.errors import VariableError
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import InlineIfHeader

        n = cast(InlineIfHeader, node)

        for assign_token in n.get_tokens(RobotToken.ASSIGN):
            variable_token = self.get_variable_token(assign_token)

            try:
                if variable_token is not None:
                    if (
                        self.position is not None
                        and self.position in range_from_node(n)
                        and self.position > range_from_token(variable_token).end
                    ):
                        continue

                    if variable_token.value not in self._results:
                        self._results[variable_token.value] = LocalVariableDefinition(
                            name=variable_token.value,
                            name_token=strip_variable_token(variable_token),
                            line_no=variable_token.lineno,
                            col_offset=variable_token.col_offset,
                            end_line_no=variable_token.lineno,
                            end_col_offset=variable_token.end_col_offset,
                            source=self.source,
                        )

            except VariableError:
                pass

    async def visit_ForHeader(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import ForHeader

        n = cast(ForHeader, node)
        variables = n.get_tokens(RobotToken.VARIABLE)
        for variable in variables:
            variable_token = self.get_variable_token(variable)
            if variable_token is not None and variable_token.value and variable_token.value not in self._results:
                self._results[variable_token.value] = LocalVariableDefinition(
                    name=variable_token.value,
                    name_token=strip_variable_token(variable_token),
                    line_no=variable_token.lineno,
                    col_offset=variable_token.col_offset,
                    end_line_no=variable_token.lineno,
                    end_col_offset=variable_token.end_col_offset,
                    source=self.source,
                )


class ImportVisitor(AsyncVisitor):
    async def get(self, source: str, model: ast.AST) -> List[Import]:
        self._results: List[Import] = []
        self.source = source
        await self.visit(model)
        return self._results

    async def visit_Section(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.model.blocks import SettingSection

        if isinstance(node, SettingSection):
            await self.generic_visit(node)

    async def visit_LibraryImport(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import LibraryImport as RobotLibraryImport

        n = cast(RobotLibraryImport, node)
        name = cast(RobotToken, n.get_token(RobotToken.NAME))

        last_data_token = cast(
            RobotToken, next(v for v in reversed(n.tokens) if v.type not in RobotToken.NON_DATA_TOKENS)
        )

        self._results.append(
            LibraryImport(
                name=n.name,
                name_token=name if name is not None else None,
                args=n.args,
                alias=n.alias,
                line_no=node.lineno,
                col_offset=node.col_offset,
                end_line_no=last_data_token.lineno
                if last_data_token is not None
                else node.end_lineno
                if node.end_lineno is not None
                else -1,
                end_col_offset=last_data_token.end_col_offset
                if last_data_token is not None
                else node.end_col_offset
                if node.end_col_offset is not None
                else -1,
                source=self.source,
            )
        )

    async def visit_ResourceImport(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import ResourceImport as RobotResourceImport

        n = cast(RobotResourceImport, node)
        name = cast(RobotToken, n.get_token(RobotToken.NAME))

        last_data_token = cast(
            RobotToken, next(v for v in reversed(n.tokens) if v.type not in RobotToken.NON_DATA_TOKENS)
        )
        self._results.append(
            ResourceImport(
                name=n.name,
                name_token=name if name is not None else None,
                line_no=node.lineno,
                col_offset=node.col_offset,
                end_line_no=last_data_token.lineno
                if last_data_token is not None
                else node.end_lineno
                if node.end_lineno is not None
                else -1,
                end_col_offset=last_data_token.end_col_offset
                if last_data_token is not None
                else node.end_col_offset
                if node.end_col_offset is not None
                else -1,
                source=self.source,
            )
        )

    async def visit_VariablesImport(self, node: ast.AST) -> None:  # noqa: N802
        from robot.parsing.lexer.tokens import Token as RobotToken
        from robot.parsing.model.statements import (
            VariablesImport as RobotVariablesImport,
        )

        n = cast(RobotVariablesImport, node)
        name = cast(RobotToken, n.get_token(RobotToken.NAME))

        last_data_token = cast(
            RobotToken, next(v for v in reversed(n.tokens) if v.type not in RobotToken.NON_DATA_TOKENS)
        )
        self._results.append(
            VariablesImport(
                name=n.name,
                name_token=name if name is not None else None,
                args=n.args,
                line_no=node.lineno,
                col_offset=node.col_offset,
                end_line_no=last_data_token.lineno
                if last_data_token is not None
                else node.end_lineno
                if node.end_lineno is not None
                else -1,
                end_col_offset=last_data_token.end_col_offset
                if last_data_token is not None
                else node.end_col_offset
                if node.end_col_offset is not None
                else -1,
                source=self.source,
            )
        )


@dataclass
class LibraryEntry:
    name: str
    import_name: str
    library_doc: LibraryDoc
    args: Tuple[Any, ...] = ()
    alias: Optional[str] = None
    import_range: Range = field(default_factory=lambda: Range.zero())
    import_source: Optional[str] = None

    def __str__(self) -> str:
        result = self.import_name
        if self.args:
            result += f"  {str(self.args)}"
        if self.alias:
            result += f"  WITH NAME  {self.alias}"
        return result


@dataclass
class ResourceEntry(LibraryEntry):
    imports: List[Import] = field(default_factory=lambda: [])
    variables: List[VariableDefinition] = field(default_factory=lambda: [])


@dataclass
class VariablesEntry(LibraryEntry):
    variables: List[VariableDefinition] = field(default_factory=lambda: [])


class DocumentType(enum.Enum):
    UNKNOWN = "unknown"
    GENERAL = "robot"
    RESOURCE = "resource"
    INIT = "init"


class Namespace:
    _logger = LoggingDescriptor()

    @_logger.call
    def __init__(
        self,
        imports_manager: ImportsManager,
        model: ast.AST,
        source: str,
        document: Optional[TextDocument] = None,
        document_type: Optional[DocumentType] = None,
        languages: Optional[Languages] = None,
        workspace_languages: Optional[Languages] = None,
    ) -> None:
        super().__init__()

        self.imports_manager = imports_manager

        self.model = model
        self.source = source
        self._document = weakref.ref(document) if document is not None else None
        self.document_type: Optional[DocumentType] = document_type
        self.languages = languages
        self.workspace_languages = workspace_languages

        self._libraries: OrderedDict[str, LibraryEntry] = OrderedDict()
        self._libraries_matchers: Optional[Dict[KeywordMatcher, LibraryEntry]] = None
        self._resources: OrderedDict[str, ResourceEntry] = OrderedDict()
        self._resources_matchers: Optional[Dict[KeywordMatcher, ResourceEntry]] = None
        self._variables: OrderedDict[str, VariablesEntry] = OrderedDict()
        self._initialized = False
        self._initialize_lock = Lock()
        self._analyzed = False
        self._analyze_lock = Lock()
        self._library_doc: Optional[LibraryDoc] = None
        self._library_doc_lock = Lock()
        self._imports: Optional[List[Import]] = None
        self._import_entries: OrderedDict[Import, LibraryEntry] = OrderedDict()
        self._own_variables: Optional[List[VariableDefinition]] = None
        self._own_variables_lock = Lock()
        self._global_variables: Optional[List[VariableDefinition]] = None
        self._global_variables_lock = Lock()

        self._diagnostics: List[Diagnostic] = []
        self._keyword_references: Dict[KeywordDoc, Set[Location]] = {}
        self._variable_references: Dict[VariableDefinition, Set[Location]] = {}

        self._keywords: Optional[List[KeywordDoc]] = None

        self._keywords_lock = Lock()

        # TODO: how to get the search order from model
        self.search_order: Tuple[str, ...] = ()

        self._finder: Optional[KeywordFinder] = None

        self.imports_manager.imports_changed.add(self.imports_changed)
        self.imports_manager.libraries_changed.add(self.libraries_changed)
        self.imports_manager.resources_changed.add(self.resources_changed)
        self.imports_manager.variables_changed.add(self.variables_changed)

        self._in_initialize = False

    @async_event
    async def has_invalidated(sender) -> None:  # NOSONAR
        ...

    @async_event
    async def has_initialized(sender) -> None:  # NOSONAR
        ...

    @async_event
    async def has_imports_changed(sender) -> None:  # NOSONAR
        ...

    @async_event
    async def has_analysed(sender) -> None:  # NOSONAR
        ...

    @property
    def document(self) -> Optional[TextDocument]:
        return self._document() if self._document is not None else None

    async def imports_changed(self, sender: Any, uri: DocumentUri) -> None:  # NOSONAR
        if self.document is not None:
            self.document.set_data(Namespace.DataEntry, None)

        await self.invalidate()

    @_logger.call
    async def libraries_changed(self, sender: Any, libraries: List[LibraryDoc]) -> None:
        for p in libraries:
            if any(e for e in self._libraries.values() if e.library_doc == p):
                if self.document is not None:
                    self.document.set_data(Namespace.DataEntry, None)
                await self.invalidate()
                break

    @_logger.call
    async def resources_changed(self, sender: Any, resources: List[LibraryDoc]) -> None:
        for p in resources:
            if any(e for e in self._resources.values() if e.library_doc.source == p.source):
                if self.document is not None:
                    self.document.set_data(Namespace.DataEntry, None)
                await self.invalidate()
                break

    @_logger.call
    async def variables_changed(self, sender: Any, variables: List[LibraryDoc]) -> None:
        for p in variables:
            if any(e for e in self._variables.values() if e.library_doc.source == p.source):
                if self.document is not None:
                    self.document.set_data(Namespace.DataEntry, None)
                await self.invalidate()
                break

    async def is_initialized(self) -> bool:
        async with self._initialize_lock:
            return self._initialized

    async def _invalidate(self) -> None:
        self._initialized = False

        self._libraries = OrderedDict()
        self._libraries_matchers = None
        self._resources = OrderedDict()
        self._resources_matchers = None
        self._variables = OrderedDict()
        self._imports = None
        self._import_entries = OrderedDict()
        self._own_variables = None
        self._keywords = None
        self._library_doc = None
        self._analyzed = False
        self._diagnostics = []
        self._keyword_references = {}
        self._variable_references = {}

        self._finder = None
        self._in_initialize = False

        await self._reset_global_variables()

    @_logger.call
    async def invalidate(self) -> None:
        async with self._initialize_lock, self._library_doc_lock, self._analyze_lock:
            await self._invalidate()
        await self.has_invalidated(self)

    @_logger.call
    async def get_diagnostisc(self) -> List[Diagnostic]:
        await self.ensure_initialized()

        await self._analyze()

        return self._diagnostics

    @_logger.call
    async def get_keyword_references(self) -> Dict[KeywordDoc, Set[Location]]:
        await self.ensure_initialized()

        await self._analyze()

        return self._keyword_references

    async def get_variable_references(self) -> Dict[VariableDefinition, Set[Location]]:
        await self.ensure_initialized()

        await self._analyze()

        return self._variable_references

    @_logger.call
    async def get_libraries(self) -> OrderedDict[str, LibraryEntry]:
        await self.ensure_initialized()

        return self._libraries

    async def get_libraries_matchers(self) -> Dict[KeywordMatcher, LibraryEntry]:
        if self._libraries_matchers is None:
            self._libraries_matchers = {
                KeywordMatcher(v.alias or v.name or v.import_name, False): v
                for v in (await self.get_libraries()).values()
            }
        return self._libraries_matchers

    async def get_resources(self) -> OrderedDict[str, ResourceEntry]:
        await self.ensure_initialized()

        return self._resources

    async def get_resources_matchers(self) -> Dict[KeywordMatcher, ResourceEntry]:
        if self._resources_matchers is None:
            self._resources_matchers = {
                KeywordMatcher(v.alias or v.name or v.import_name, False): v
                for v in (await self.get_resources()).values()
            }
        return self._resources_matchers

    async def get_imported_variables(self) -> OrderedDict[str, VariablesEntry]:
        await self.ensure_initialized()

        return self._variables

    @_logger.call
    async def get_library_doc(self) -> LibraryDoc:
        async with self._library_doc_lock:
            if self._library_doc is None:
                self._library_doc = await self.imports_manager.get_libdoc_from_model(
                    self.model,
                    self.source,
                    model_type="RESOURCE",
                    append_model_errors=self.document_type is not None
                    and self.document_type in [DocumentType.RESOURCE],
                )

            return self._library_doc

    class DataEntry(NamedTuple):
        libraries: OrderedDict[str, LibraryEntry] = OrderedDict()
        resources: OrderedDict[str, ResourceEntry] = OrderedDict()
        variables: OrderedDict[str, VariablesEntry] = OrderedDict()
        diagnostics: List[Diagnostic] = []
        import_entries: OrderedDict[Import, LibraryEntry] = OrderedDict()

    @_logger.call(condition=lambda self: not self._initialized)
    async def ensure_initialized(self) -> bool:
        async with self._initialize_lock:
            imports_changed = False

            if not self._initialized:

                if self._in_initialize:
                    self._logger.critical(f"already initialized {self.document}")

                self._in_initialize = True

                try:
                    self._logger.debug(f"ensure_initialized -> initialize {self.document}")

                    imports = await self.get_imports()

                    data_entry: Optional[Namespace.DataEntry] = None
                    if self.document is not None:
                        # check or save several data in documents data cache,
                        # if imports are different, then the data is invalid
                        old_imports: List[Import] = self.document.get_data(Namespace)
                        if old_imports is None:
                            self.document.set_data(Namespace, imports)
                        elif old_imports != imports:
                            imports_changed = True

                            new_imports = []
                            for e in old_imports:
                                if e in imports:
                                    new_imports.append(e)
                            for e in imports:
                                if e not in new_imports:
                                    new_imports.append(e)
                            self.document.set_data(Namespace, new_imports)
                            self.document.set_data(Namespace.DataEntry, None)
                        else:
                            data_entry = self.document.get_data(Namespace.DataEntry)

                    if data_entry is not None:
                        self._libraries = data_entry.libraries.copy()
                        self._resources = data_entry.resources.copy()
                        self._variables = data_entry.variables.copy()
                        self._diagnostics = data_entry.diagnostics.copy()
                        self._import_entries = data_entry.import_entries.copy()
                    else:

                        variables = await self.get_resolvable_variables()

                        await self._import_default_libraries(variables)
                        await self._import_imports(
                            imports, str(Path(self.source).parent), top_level=True, variables=variables
                        )

                        if self.document is not None:
                            self.document.set_data(
                                Namespace.DataEntry,
                                Namespace.DataEntry(
                                    self._libraries.copy(),
                                    self._resources.copy(),
                                    self._variables.copy(),
                                    self._diagnostics.copy(),
                                    self._import_entries.copy(),
                                ),
                            )

                    await self._reset_global_variables()

                    self._initialized = True

                except BaseException as e:
                    if not isinstance(e, asyncio.CancelledError):
                        self._logger.exception(e, level=logging.DEBUG)

                    if self.document is not None:
                        self.document.remove_data(Namespace)
                        self.document.remove_data(Namespace.DataEntry)

                    await self._invalidate()
                    raise
                finally:
                    self._in_initialize = False

        if self._initialized:
            await self.has_initialized(self)

            if imports_changed:
                await self.has_imports_changed(self)

        return self._initialized

    @property
    def initialized(self) -> bool:
        return self._initialized

    @_logger.call
    async def get_imports(self) -> List[Import]:
        if self._imports is None:
            self._imports = await ImportVisitor().get(self.source, self.model)

        return self._imports

    @_logger.call
    async def get_own_variables(self) -> List[VariableDefinition]:
        async with self._own_variables_lock:
            if self._own_variables is None:
                self._own_variables = await VariablesVisitor().get(self.source, self.model)

            return self._own_variables

    _builtin_variables: Optional[List[BuiltInVariableDefinition]] = None

    @classmethod
    def get_builtin_variables(cls) -> List[BuiltInVariableDefinition]:
        if cls._builtin_variables is None:
            cls._builtin_variables = [BuiltInVariableDefinition(0, 0, 0, 0, "", n, None) for n in BUILTIN_VARIABLES]

        return cls._builtin_variables

    @_logger.call
    async def get_command_line_variables(self) -> List[VariableDefinition]:
        return await self.imports_manager.get_command_line_variables()

    async def _reset_global_variables(self) -> None:
        async with self._global_variables_lock:
            self._global_variables = None

    async def get_global_variables(self) -> List[VariableDefinition]:
        async with self._global_variables_lock:
            if self._global_variables is None:
                self._global_variables = list(
                    itertools.chain(
                        await self.get_command_line_variables(),
                        await self.get_own_variables(),
                        *(e.variables for e in self._resources.values()),
                        *(e.variables for e in self._variables.values()),
                        self.get_builtin_variables(),
                    )
                )

            return self._global_variables

    async def yield_variables(
        self,
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
        skip_commandline_variables: bool = False,
    ) -> AsyncGenerator[Tuple[VariableMatcher, VariableDefinition], None]:
        from robot.parsing.model.blocks import Keyword, TestCase
        from robot.parsing.model.statements import Arguments

        yielded: Dict[VariableMatcher, VariableDefinition] = {}

        test_or_keyword_nodes = list(
            itertools.dropwhile(lambda v: not isinstance(v, (TestCase, Keyword)), nodes if nodes else [])
        )
        test_or_keyword = test_or_keyword_nodes[0] if test_or_keyword_nodes else None

        for var in chain(
            *[
                (
                    await BlockVariableVisitor(
                        self,
                        self.source,
                        position,
                        isinstance(test_or_keyword_nodes[-1], Arguments) if nodes else False,
                    ).get(test_or_keyword)
                )
                if test_or_keyword is not None
                else []
            ],
            await self.get_global_variables(),
        ):
            if var.matcher not in yielded.keys():
                yielded[var.matcher] = var

                if skip_commandline_variables and isinstance(var, CommandLineVariableDefinition):
                    continue

                yield var.matcher, var

    async def get_resolvable_variables(
        self, nodes: Optional[List[ast.AST]] = None, position: Optional[Position] = None
    ) -> Dict[str, Any]:
        return {
            v.name: v.value
            async for k, v in self.yield_variables(nodes, position, skip_commandline_variables=True)
            if v.has_value
        }

    async def get_variable_matchers(
        self, nodes: Optional[List[ast.AST]] = None, position: Optional[Position] = None
    ) -> Dict[VariableMatcher, VariableDefinition]:
        await self.ensure_initialized()

        return {m: v async for m, v in self.yield_variables(nodes, position)}

    @_logger.call
    async def find_variable(
        self,
        name: str,
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
        skip_commandline_variables: bool = False,
        ignore_error: bool = False,
    ) -> Optional[VariableDefinition]:

        await self.ensure_initialized()

        if name[:2] == "%{" and name[-1] == "}":
            return EnvironmentVariableDefinition(0, 0, 0, 0, "", name, None)

        try:
            matcher = VariableMatcher(name)

            async for m, v in self.yield_variables(
                nodes,
                position,
                skip_commandline_variables=skip_commandline_variables,
            ):
                if matcher == m:
                    return v
        except InvalidVariableError:
            if not ignore_error:
                raise

        return None

    async def _import_imports(
        self,
        imports: Iterable[Import],
        base_dir: str,
        *,
        top_level: bool = False,
        variables: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        parent_import: Optional[Import] = None,
    ) -> None:
        async def _import(
            value: Import, variables: Optional[Dict[str, Any]] = None
        ) -> Tuple[Optional[LibraryEntry], Optional[Dict[str, Any]]]:
            result: Optional[LibraryEntry] = None
            try:
                if isinstance(value, LibraryImport):
                    if value.name is None:
                        raise NameSpaceError("Library setting requires value.")

                    result = await self._get_library_entry(
                        value.name, value.args, value.alias, base_dir, sentinel=value, variables=variables
                    )
                    result.import_range = value.range
                    result.import_source = value.source

                    self._import_entries[value] = result

                    if (
                        top_level
                        and result.library_doc.errors is None
                        and (len(result.library_doc.keywords) == 0 and not bool(result.library_doc.has_listener))
                    ):
                        await self.append_diagnostics(
                            range=value.range,
                            message=f"Imported library '{value.name}' contains no keywords.",
                            severity=DiagnosticSeverity.WARNING,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            code="LibraryContainsNoKeywords",
                        )
                elif isinstance(value, ResourceImport):
                    if value.name is None:
                        raise NameSpaceError("Resource setting requires value.")

                    source = await self.imports_manager.find_resource(value.name, base_dir, variables=variables)

                    if self.source == source:
                        if parent_import:
                            await self.append_diagnostics(
                                range=parent_import.range,
                                message="Possible circular import.",
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=[
                                    DiagnosticRelatedInformation(
                                        location=Location(str(Uri.from_path(value.source)), value.range),
                                        message=f"'{Path(self.source).name}' is also imported here.",
                                    )
                                ]
                                if value.source
                                else None,
                                code="PossibleCircularImport",
                            )
                    else:
                        result = await self._get_resource_entry(
                            value.name, base_dir, sentinel=value, variables=variables
                        )
                        result.import_range = value.range
                        result.import_source = value.source

                        self._import_entries[value] = result
                        if result.variables:
                            variables = None

                        if top_level and (
                            not result.library_doc.errors
                            and top_level
                            and not result.imports
                            and not result.variables
                            and not result.library_doc.keywords
                        ):
                            await self.append_diagnostics(
                                range=value.range,
                                message=f"Imported resource file '{value.name}' is empty.",
                                severity=DiagnosticSeverity.WARNING,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                code="ResourceEmpty",
                            )

                elif isinstance(value, VariablesImport):

                    if value.name is None:
                        raise NameSpaceError("Variables setting requires value.")

                    result = await self._get_variables_entry(
                        value.name, value.args, base_dir, sentinel=value, variables=variables
                    )

                    result.import_range = value.range
                    result.import_source = value.source

                    self._import_entries[value] = result
                    variables = None
                else:
                    raise DiagnosticsError("Unknown import type.")

                if top_level and result is not None:
                    if result.library_doc.source is not None and result.library_doc.errors:
                        if any(err.source and Path(err.source).is_absolute() for err in result.library_doc.errors):
                            await self.append_diagnostics(
                                range=value.range,
                                message="Import definition contains errors.",
                                severity=DiagnosticSeverity.ERROR,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=[
                                    DiagnosticRelatedInformation(
                                        location=Location(
                                            uri=str(Uri.from_path(err.source)),
                                            range=Range(
                                                start=Position(
                                                    line=err.line_no - 1
                                                    if err.line_no is not None
                                                    else result.library_doc.line_no
                                                    if result.library_doc.line_no >= 0
                                                    else 0,
                                                    character=0,
                                                ),
                                                end=Position(
                                                    line=err.line_no - 1
                                                    if err.line_no is not None
                                                    else result.library_doc.line_no
                                                    if result.library_doc.line_no >= 0
                                                    else 0,
                                                    character=0,
                                                ),
                                            ),
                                        ),
                                        message=err.message,
                                    )
                                    for err in result.library_doc.errors
                                    if err.source is not None
                                ],
                                code="ImportContainsErrors",
                            )
                        for err in filter(
                            lambda e: e.source is None or not Path(e.source).is_absolute(), result.library_doc.errors
                        ):
                            await self.append_diagnostics(
                                range=value.range,
                                message=err.message,
                                severity=DiagnosticSeverity.ERROR,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                code=err.type_name,
                            )
                    elif result.library_doc.errors is not None:
                        for err in result.library_doc.errors:
                            await self.append_diagnostics(
                                range=value.range,
                                message=err.message,
                                severity=DiagnosticSeverity.ERROR,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                code=err.type_name,
                            )

            except (asyncio.CancelledError, SystemExit, KeyboardInterrupt):
                raise
            except BaseException as e:
                if top_level:
                    await self.append_diagnostics(
                        range=value.range,
                        message=str(e),
                        severity=DiagnosticSeverity.ERROR,
                        source=DIAGNOSTICS_SOURCE_NAME,
                        code=type(e).__qualname__,
                    )
            finally:
                await self._reset_global_variables()

            return result, variables

        current_time = time.monotonic()
        self._logger.debug(lambda: f"start imports for {self.document if top_level else source}")
        try:

            async for imp in as_async_iterable(imports):
                if variables is None:
                    variables = await self.get_resolvable_variables()

                entry, variables = await _import(imp, variables=variables)

                if entry is not None:
                    if isinstance(entry, ResourceEntry):
                        assert entry.library_doc.source is not None
                        already_imported_resources = next(
                            (e for e in self._resources.values() if e.library_doc.source == entry.library_doc.source),
                            None,
                        )

                        if already_imported_resources is None and entry.library_doc.source != self.source:
                            self._resources[entry.import_name] = entry
                            try:
                                await self._import_imports(
                                    entry.imports,
                                    str(Path(entry.library_doc.source).parent),
                                    top_level=False,
                                    variables=variables,
                                    source=entry.library_doc.source,
                                    parent_import=imp if top_level else parent_import,
                                )
                            except (asyncio.CancelledError, SystemExit, KeyboardInterrupt):
                                raise
                            except BaseException as e:
                                if top_level:
                                    await self.append_diagnostics(
                                        range=entry.import_range,
                                        message=str(e) or type(entry).__name__,
                                        severity=DiagnosticSeverity.ERROR,
                                        source=DIAGNOSTICS_SOURCE_NAME,
                                        code=type(e).__qualname__,
                                    )
                        else:
                            if top_level:
                                if entry.library_doc.source == self.source:
                                    await self.append_diagnostics(
                                        range=entry.import_range,
                                        message="Recursive resource import.",
                                        severity=DiagnosticSeverity.INFORMATION,
                                        source=DIAGNOSTICS_SOURCE_NAME,
                                        code="RecursiveImport",
                                    )
                                elif (
                                    already_imported_resources is not None
                                    and already_imported_resources.library_doc.source
                                ):
                                    await self.append_diagnostics(
                                        range=entry.import_range,
                                        message=f"Resource {entry} already imported.",
                                        severity=DiagnosticSeverity.INFORMATION,
                                        source=DIAGNOSTICS_SOURCE_NAME,
                                        related_information=[
                                            DiagnosticRelatedInformation(
                                                location=Location(
                                                    uri=str(Uri.from_path(already_imported_resources.import_source)),
                                                    range=already_imported_resources.import_range,
                                                ),
                                                message="",
                                            )
                                        ]
                                        if already_imported_resources.import_source
                                        else None,
                                        code="ResourceAlreadyImported",
                                    )

                    elif isinstance(entry, VariablesEntry):
                        already_imported_variables = [
                            e
                            for e in self._variables.values()
                            if e.library_doc.source == entry.library_doc.source
                            and e.alias == entry.alias
                            and e.args == entry.args
                        ]
                        if (
                            top_level
                            and already_imported_variables
                            and already_imported_variables[0].library_doc.source
                        ):
                            await self.append_diagnostics(
                                range=entry.import_range,
                                message=f'Variables "{entry}" already imported.',
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=[
                                    DiagnosticRelatedInformation(
                                        location=Location(
                                            uri=str(Uri.from_path(already_imported_variables[0].import_source)),
                                            range=already_imported_variables[0].import_range,
                                        ),
                                        message="",
                                    )
                                ]
                                if already_imported_variables[0].import_source
                                else None,
                                code="VariablesAlreadyImported",
                            )

                        if (entry.alias or entry.name or entry.import_name) not in self._variables:
                            self._variables[entry.alias or entry.name or entry.import_name] = entry

                    elif isinstance(entry, LibraryEntry):
                        if top_level and entry.name == BUILTIN_LIBRARY_NAME and entry.alias is None:
                            await self.append_diagnostics(
                                range=entry.import_range,
                                message=f'Library "{entry}" is not imported,'
                                ' because it would override the "BuiltIn" library.',
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=[
                                    DiagnosticRelatedInformation(
                                        location=Location(
                                            uri=str(Uri.from_path(entry.import_source)),
                                            range=entry.import_range,
                                        ),
                                        message="",
                                    )
                                ]
                                if entry.import_source
                                else None,
                                code="LibraryOverridesBuiltIn",
                            )
                            continue

                        already_imported_library = [
                            e
                            for e in self._libraries.values()
                            if e.library_doc.source == entry.library_doc.source
                            and e.alias == entry.alias
                            and e.args == entry.args
                        ]
                        if top_level and already_imported_library and already_imported_library[0].library_doc.source:
                            await self.append_diagnostics(
                                range=entry.import_range,
                                message=f'Library "{entry}" already imported.',
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=[
                                    DiagnosticRelatedInformation(
                                        location=Location(
                                            uri=str(Uri.from_path(already_imported_library[0].import_source)),
                                            range=already_imported_library[0].import_range,
                                        ),
                                        message="",
                                    )
                                ]
                                if already_imported_library[0].import_source
                                else None,
                                code="LibraryAlreadyImported",
                            )

                        if (entry.alias or entry.name or entry.import_name) not in self._libraries:
                            self._libraries[entry.alias or entry.name or entry.import_name] = entry
        finally:
            self._logger.debug(
                lambda: "end import imports for "
                + f"{self.document if top_level else source} in {time.monotonic() - current_time}s"
            )

    async def _import_default_libraries(self, variables: Optional[Dict[str, Any]] = None) -> None:
        async def _import_lib(library: str, variables: Optional[Dict[str, Any]] = None) -> Optional[LibraryEntry]:
            try:
                return await self._get_library_entry(
                    library, (), None, str(Path(self.source).parent), is_default_library=True, variables=variables
                )
            except (asyncio.CancelledError, SystemExit, KeyboardInterrupt):
                raise
            except BaseException as e:
                await self.append_diagnostics(
                    range=Range.zero(),
                    message=f"Can't import default library '{library}': {str(e) or type(e).__name__}",
                    severity=DiagnosticSeverity.ERROR,
                    source="Robot",
                    code=type(e).__qualname__,
                )
                return None

        self._logger.debug(lambda: f"start import default libraries for document {self.document}")
        try:
            for library in DEFAULT_LIBRARIES:
                e = await _import_lib(library, variables or await self.get_resolvable_variables())
                if e is not None:
                    self._libraries[e.alias or e.name or e.import_name] = e
        finally:
            self._logger.debug(lambda: f"end import default libraries for document {self.document}")

    @_logger.call
    async def _get_library_entry(
        self,
        name: str,
        args: Tuple[Any, ...],
        alias: Optional[str],
        base_dir: str,
        *,
        is_default_library: bool = False,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> LibraryEntry:

        library_doc = await self.imports_manager.get_libdoc_for_library_import(
            name,
            args,
            base_dir=base_dir,
            sentinel=None if is_default_library else sentinel,
            variables=variables or await self.get_resolvable_variables(),
        )

        return LibraryEntry(name=library_doc.name, import_name=name, library_doc=library_doc, args=args, alias=alias)

    @_logger.call
    async def get_imported_library_libdoc(
        self, name: str, args: Tuple[str, ...] = (), alias: Optional[str] = None
    ) -> Optional[LibraryDoc]:
        await self.ensure_initialized()

        return next(
            (
                v.library_doc
                for e, v in self._import_entries.items()
                if isinstance(e, LibraryImport) and v.import_name == name and v.args == args and v.alias == alias
            ),
            None,
        )

    @_logger.call
    async def _get_resource_entry(
        self, name: str, base_dir: str, *, sentinel: Any = None, variables: Optional[Dict[str, Any]] = None
    ) -> ResourceEntry:
        namespace, library_doc = await self.imports_manager.get_namespace_and_libdoc_for_resource_import(
            name,
            base_dir,
            sentinel=sentinel,
            variables=variables or await self.get_resolvable_variables(),
        )

        return ResourceEntry(
            name=library_doc.name,
            import_name=name,
            library_doc=library_doc,
            imports=await namespace.get_imports(),
            variables=await namespace.get_own_variables(),
        )

    @_logger.call
    async def get_imported_resource_libdoc(self, name: str) -> Optional[LibraryDoc]:
        await self.ensure_initialized()

        return next(
            (
                v.library_doc
                for e, v in self._import_entries.items()
                if isinstance(e, ResourceImport) and v.import_name == name
            ),
            None,
        )

    @_logger.call
    async def _get_variables_entry(
        self,
        name: str,
        args: Tuple[Any, ...],
        base_dir: str,
        *,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> VariablesEntry:
        library_doc = await self.imports_manager.get_libdoc_for_variables_import(
            name,
            args,
            base_dir=base_dir,
            sentinel=sentinel,
            variables=variables or await self.get_resolvable_variables(),
        )

        return VariablesEntry(
            name=library_doc.name, import_name=name, library_doc=library_doc, args=args, variables=library_doc.variables
        )

    @_logger.call
    async def get_imported_variables_libdoc(self, name: str, args: Tuple[str, ...] = ()) -> Optional[LibraryDoc]:
        await self.ensure_initialized()

        return next(
            (
                v.library_doc
                for e, v in self._import_entries.items()
                if isinstance(e, VariablesImport) and v.import_name == name and v.args == args
            ),
            None,
        )

    @_logger.call
    async def iter_all_keywords(self) -> AsyncGenerator[KeywordDoc, None]:
        import itertools

        libdoc = await self.get_library_doc()

        for doc in itertools.chain(
            *(e.library_doc.keywords.values() for e in self._libraries.values()),
            *(e.library_doc.keywords.values() for e in self._resources.values()),
            libdoc.keywords.values() if libdoc is not None else [],
        ):
            yield doc

    @_logger.call
    async def get_keywords(self) -> List[KeywordDoc]:
        async with self._keywords_lock:
            if self._keywords is None:

                current_time = time.monotonic()
                self._logger.debug("start collecting keywords")
                try:
                    i = 0

                    await self.ensure_initialized()

                    result: Dict[KeywordMatcher, KeywordDoc] = {}

                    async for doc in self.iter_all_keywords():
                        i += 1
                        result[KeywordMatcher(doc.name)] = doc

                    self._keywords = list(result.values())
                finally:
                    self._logger.debug(
                        lambda: f"end collecting {len(self._keywords) if self._keywords else 0}"
                        f" keywords in {time.monotonic()-current_time}s analyze {i} keywords"
                    )

            return self._keywords

    async def append_diagnostics(
        self,
        range: Range,
        message: str,
        severity: Optional[DiagnosticSeverity] = None,
        code: Union[int, str, None] = None,
        code_description: Optional[CodeDescription] = None,
        source: Optional[str] = None,
        tags: Optional[List[DiagnosticTag]] = None,
        related_information: Optional[List[DiagnosticRelatedInformation]] = None,
        data: Optional[Any] = None,
    ) -> None:
        from .analyzer import Analyzer

        if await Analyzer.should_ignore(self.document, range):
            return

        self._diagnostics.append(
            Diagnostic(range, message, severity, code, code_description, source, tags, related_information, data)
        )

    async def is_analyzed(self) -> bool:
        async with self._analyze_lock:
            return self._analyzed

    @_logger.call(condition=lambda self: not self._analyzed)
    async def _analyze(self) -> None:
        import time

        from .analyzer import Analyzer

        async with self._analyze_lock:
            if not self._analyzed:
                canceled = False

                self._logger.debug(lambda: f"start analyze {self.document}")
                start_time = time.monotonic()

                try:
                    result = await Analyzer(self.model, self).run()

                    self._diagnostics += result.diagnostics
                    self._keyword_references = result.keyword_references
                    self._variable_references = result.variable_references

                    lib_doc = await self.get_library_doc()

                    if lib_doc.errors is not None:
                        for err in lib_doc.errors:
                            await self.append_diagnostics(
                                range=Range(
                                    start=Position(
                                        line=((err.line_no - 1) if err.line_no is not None else 0),
                                        character=0,
                                    ),
                                    end=Position(
                                        line=((err.line_no - 1) if err.line_no is not None else 0),
                                        character=0,
                                    ),
                                ),
                                message=err.message,
                                severity=DiagnosticSeverity.ERROR,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                code=err.type_name,
                            )

                except asyncio.CancelledError:
                    canceled = True
                    self._logger.debug("analyzing canceled")
                    raise
                finally:
                    self._analyzed = not canceled

                    self._logger.debug(
                        lambda: f"end analyzed {self.document} succeed in {time.monotonic() - start_time}s"
                        if self._analyzed
                        else f"end analyzed {self.document} failed in {time.monotonic() - start_time}s"
                    )

                await self.has_analysed(self)

    async def get_finder(self) -> KeywordFinder:
        if self._finder is None:
            await self.ensure_initialized()
            self._finder = KeywordFinder(self)
        return self._finder

    @_logger.call(condition=lambda self, name, **kwargs: self._finder is not None and name not in self._finder._cache)
    async def find_keyword(
        self, name: Optional[str], *, raise_keyword_error: bool = True, handle_bdd_style: bool = True
    ) -> Optional[KeywordDoc]:
        finder = self._finder if self._finder is not None else await self.get_finder()

        return await finder.find_keyword(
            name, raise_keyword_error=raise_keyword_error, handle_bdd_style=handle_bdd_style
        )


class DiagnosticsEntry(NamedTuple):
    message: str
    severity: DiagnosticSeverity
    code: Optional[str] = None


class CancelSearchError(Exception):
    pass


DEFAULT_BDD_PREFIXES = {"Given ", "When ", "Then ", "And ", "But "}


class KeywordFinder:
    def __init__(self, namespace: Namespace) -> None:
        super().__init__()
        self.namespace = namespace
        self.diagnostics: List[DiagnosticsEntry] = []
        self.self_library_doc: Optional[LibraryDoc] = None
        self._cache: Dict[Tuple[Optional[str], bool], Tuple[Optional[KeywordDoc], List[DiagnosticsEntry]]] = {}
        self.handle_bdd_style = True
        self._all_keywords: Optional[List[LibraryEntry]] = None
        self._resource_keywords: Optional[List[ResourceEntry]] = None
        self._library_keywords: Optional[List[LibraryEntry]] = None

    def reset_diagnostics(self) -> None:
        self.diagnostics = []

    async def find_keyword(
        self, name: Optional[str], *, raise_keyword_error: bool = False, handle_bdd_style: bool = True
    ) -> Optional[KeywordDoc]:
        try:
            self.reset_diagnostics()

            self.handle_bdd_style = handle_bdd_style

            cached = self._cache.get((name, self.handle_bdd_style), None)

            if cached is not None:
                self.diagnostics = cached[1]
                return cached[0]
            else:
                try:
                    result = await self._find_keyword(name)
                    if result is None:
                        self.diagnostics.append(
                            DiagnosticsEntry(
                                f"No keyword with name {repr(name)} found.", DiagnosticSeverity.ERROR, "KeywordError"
                            )
                        )
                except KeywordError as e:
                    if raise_keyword_error:
                        raise

                    result = None
                    self.diagnostics.append(DiagnosticsEntry(str(e), DiagnosticSeverity.ERROR, "KeywordError"))

                self._cache[(name, self.handle_bdd_style)] = (result, self.diagnostics)

                return result
        except CancelSearchError:
            return None

    async def _find_keyword(self, name: Optional[str]) -> Optional[KeywordDoc]:
        if not name:
            self.diagnostics.append(
                DiagnosticsEntry("Keyword name cannot be empty.", DiagnosticSeverity.ERROR, "KeywordError")
            )
            raise CancelSearchError()
        if not isinstance(name, str):
            self.diagnostics.append(
                DiagnosticsEntry("Keyword name must be a string.", DiagnosticSeverity.ERROR, "KeywordError")
            )
            raise CancelSearchError()

        result = await self._get_keyword_from_self(name)
        if not result and "." in name:
            result = await self._get_explicit_keyword(name)

        if not result:
            result = await self._get_implicit_keyword(name)

        if not result and self.handle_bdd_style:
            result = await self._get_bdd_style_keyword(name)

        return result

    async def _get_keyword_from_self(self, name: str) -> Optional[KeywordDoc]:
        if self.self_library_doc is None:
            self.self_library_doc = await self.namespace.get_library_doc()
        try:
            return self.self_library_doc.keywords.get(name, None)
        except KeywordError as e:
            self.diagnostics.append(
                DiagnosticsEntry(
                    str(e),
                    DiagnosticSeverity.ERROR,
                    "KeywordError",
                )
            )
            raise CancelSearchError() from e

    async def _yield_owner_and_kw_names(self, full_name: str) -> AsyncGenerator[Tuple[str, ...], None]:
        tokens = full_name.split(".")
        for i in range(1, len(tokens)):
            yield ".".join(tokens[:i]), ".".join(tokens[i:])

    async def _get_explicit_keyword(self, name: str) -> Optional[KeywordDoc]:
        found: List[Tuple[LibraryEntry, KeywordDoc]] = []
        async for owner_name, kw_name in self._yield_owner_and_kw_names(name):
            found.extend(await self.find_keywords(owner_name, kw_name))
        if len(found) > 1:
            self.diagnostics.append(
                DiagnosticsEntry(
                    self._create_multiple_keywords_found_message(name, found, implicit=False),
                    DiagnosticSeverity.ERROR,
                    "KeywordError",
                )
            )
            raise CancelSearchError()

        return found[0][1] if found else None

    async def find_keywords(self, owner_name: str, name: str) -> Sequence[Tuple[LibraryEntry, KeywordDoc]]:
        if self._all_keywords is None:
            self._all_keywords = [
                v for v in chain(self.namespace._libraries.values(), self.namespace._resources.values())
            ]
        return [
            (v, v.library_doc.keywords[name])
            for v in self._all_keywords
            if eq(v.alias or v.name, owner_name) and name in v.library_doc.keywords
        ]

    def _create_multiple_keywords_found_message(
        self, name: str, found: Sequence[Tuple[LibraryEntry, KeywordDoc]], implicit: bool = True
    ) -> str:

        error = "Multiple keywords with name '%s' found" % name
        if implicit:
            error += ". Give the full name of the keyword you want to use"
        names = sorted(f"{e[0].alias or e[0].name}.{e[1].name}" for e in found)
        return "\n    ".join([error + ":"] + names)

    async def _get_implicit_keyword(self, name: str) -> Optional[KeywordDoc]:
        result = await self._get_keyword_from_resource_files(name)
        if not result:
            result = await self._get_keyword_from_libraries(name)
        return result

    async def _get_keyword_from_resource_files(self, name: str) -> Optional[KeywordDoc]:
        if self._resource_keywords is None:
            self._resource_keywords = [v for v in chain(self.namespace._resources.values())]

        found: List[Tuple[LibraryEntry, KeywordDoc]] = [
            (v, v.library_doc.keywords[name]) for v in self._resource_keywords if name in v.library_doc.keywords
        ]
        if not found:
            return None
        if len(found) > 1:
            found = await self._get_keyword_based_on_search_order(found)
        if len(found) == 1:
            return found[0][1]

        self.diagnostics.append(
            DiagnosticsEntry(
                self._create_multiple_keywords_found_message(name, found),
                DiagnosticSeverity.ERROR,
                "KeywordError",
            )
        )
        raise CancelSearchError()

    async def _get_keyword_based_on_search_order(
        self, entries: List[Tuple[LibraryEntry, KeywordDoc]]
    ) -> List[Tuple[LibraryEntry, KeywordDoc]]:

        for libname in self.namespace.search_order:
            for e in entries:
                if eq(libname, e[0].alias or e[0].name):
                    return [e]

        return entries

    async def _get_keyword_from_libraries(self, name: str) -> Optional[KeywordDoc]:
        if self._library_keywords is None:
            self._library_keywords = [v for v in chain(self.namespace._libraries.values())]
        found = [(v, v.library_doc.keywords[name]) for v in self._library_keywords if name in v.library_doc.keywords]
        if not found:
            return None
        if len(found) > 1:
            found = await self._get_keyword_based_on_search_order(found)
        if len(found) == 2:
            found = await self._filter_stdlib_runner(*found)
        if len(found) == 1:
            return found[0][1]

        self.diagnostics.append(
            DiagnosticsEntry(
                self._create_multiple_keywords_found_message(name, found),
                DiagnosticSeverity.ERROR,
                "KeywordError",
            )
        )
        raise CancelSearchError()

    async def _filter_stdlib_runner(
        self, entry1: Tuple[LibraryEntry, KeywordDoc], entry2: Tuple[LibraryEntry, KeywordDoc]
    ) -> List[Tuple[LibraryEntry, KeywordDoc]]:
        from robot.libraries import STDLIBS

        stdlibs_without_remote = STDLIBS - {"Remote"}
        if entry1[0].name in stdlibs_without_remote:
            standard, custom = entry1, entry2
        elif entry2[0].name in stdlibs_without_remote:
            standard, custom = entry2, entry1
        else:
            return [entry1, entry2]

        self.diagnostics.append(
            DiagnosticsEntry(
                self._create_custom_and_standard_keyword_conflict_warning_message(custom, standard),
                DiagnosticSeverity.WARNING,
                "KeywordError",
            )
        )

        return [custom]

    def _create_custom_and_standard_keyword_conflict_warning_message(
        self, custom: Tuple[LibraryEntry, KeywordDoc], standard: Tuple[LibraryEntry, KeywordDoc]
    ) -> str:
        custom_with_name = standard_with_name = ""
        if custom[0].alias is not None:
            custom_with_name = " imported as '%s'" % custom[0].alias
        if standard[0].alias is not None:
            standard_with_name = " imported as '%s'" % standard[0].alias
        return (
            f"Keyword '{standard[1].name}' found both from a custom test library "
            f"'{custom[0].name}'{custom_with_name} and a standard library '{standard[1].name}'{standard_with_name}. "
            f"The custom keyword is used. To select explicitly, and to get "
            f"rid of this warning, use either '{custom[0].alias or custom[0].name}.{custom[1].name}' "
            f"or '{standard[0].alias or standard[0].name}.{standard[1].name}'."
        )

    async def _get_bdd_style_keyword(self, name: str) -> Optional[KeywordDoc]:
        if get_robot_version() < (6, 0):
            lower = name.lower()
            for prefix in ["given ", "when ", "then ", "and ", "but "]:
                if lower.startswith(prefix):
                    return await self._find_keyword(name[len(prefix) :])  # noqa: E203
            return None

        else:
            parts = name.split()
            if len(parts) < 2:
                return None
            for index in range(1, len(parts)):
                prefix = " ".join(parts[:index]).title()
                if prefix.title() in (
                    self.namespace.languages.bdd_prefixes
                    if self.namespace.languages is not None
                    else DEFAULT_BDD_PREFIXES
                ):
                    return await self._find_keyword(" ".join(parts[index:]))
            return None
