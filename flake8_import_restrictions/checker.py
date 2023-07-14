import argparse
import ast
import fnmatch
from collections import defaultdict

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata
from typing import Dict, Iterable, List, Tuple, Union

import flake8.options.manager

from flake8_import_restrictions.imports_submodule import imports_submodule

ALL_ERRORS = {
    200,
    201,
    202,
    220,
    221,
    222,
    223,
    240,
    241,
    242,
    243,
    244,
    245,
}
DEFAULT_INCLUDE = {
    200: ["*"],
    201: ["*"],
    202: ["*"],
    221: ["*"],
    223: ["*"],
    241: ["*"],
    243: ["*"],
}
DEFAULT_EXCLUDE = {241: ["typing"]}


class ImportChecker:
    """
    A flake8 plugin used to disallow certain forms of imports.
    """

    name = "flake8-import-restrictions"
    version = metadata.version(name)
    targetted_modules: Dict[int, Tuple[List[str], List[str]]] = defaultdict(
        lambda: ([], [])
    )

    def __init__(self, tree: ast.AST, filename: str):
        self.tree = tree
        assert isinstance(filename, str)
        self.filename = filename

    @staticmethod
    def add_options(option_manager: flake8.options.manager.OptionManager):
        for error in ALL_ERRORS:
            option_manager.add_option(
                f"--imr{error}_include",
                type=str,
                comma_separated_list=True,
                default=DEFAULT_INCLUDE.get(error, []),
                parse_from_config=True,
                help=f"List of modules that IMR{error} is applied to. Allows UNIX wildcards.",
            )
            option_manager.add_option(
                f"--imr{error}_exclude",
                type=str,
                comma_separated_list=True,
                default=DEFAULT_EXCLUDE.get(error, []),
                parse_from_config=True,
                help=f"List of modules that IMR{error} is *not* applied to. Overwrites the _include flag. Allows UNIX wildcards.",
            )

    @staticmethod
    def parse_options(
        option_manager: flake8.options.manager.OptionManager,
        options: argparse.Namespace,
        extra_args,
    ):
        for error in ALL_ERRORS:
            ImportChecker.targetted_modules[error] = (
                getattr(options, f"imr{error}_include"),
                getattr(options, f"imr{error}_exclude"),
            )

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.ClassDef)
                or isinstance(node, ast.FunctionDef)
                or isinstance(node, ast.AsyncFunctionDef)
            ):
                yield from _imr200(node, ImportChecker.targetted_modules[200])

            if isinstance(node, ast.Import):
                if _applies_to(node, ImportChecker.targetted_modules[201]):
                    yield from _imr201(node)
                if _applies_to(node, ImportChecker.targetted_modules[202]):
                    yield from _imr202(node)
                if _applies_to(node, ImportChecker.targetted_modules[220]):
                    yield from _imr220(node)
                if _applies_to(node, ImportChecker.targetted_modules[221]):
                    yield from _imr221(node)
                if _applies_to(node, ImportChecker.targetted_modules[222]):
                    yield from _imr222(node)
                if _applies_to(node, ImportChecker.targetted_modules[223]):
                    yield from _imr223(node)

            if isinstance(node, ast.ImportFrom):
                if _applies_to(node, ImportChecker.targetted_modules[201]):
                    yield from _imr201(node)
                if _applies_to(node, ImportChecker.targetted_modules[202]):
                    yield from _imr202(node)
                if _applies_to(node, ImportChecker.targetted_modules[240]):
                    yield from _imr240(node)
                if _applies_to(node, ImportChecker.targetted_modules[241]):
                    yield from _imr241(node, self.filename)
                if _applies_to(node, ImportChecker.targetted_modules[242]):
                    yield from _imr242(node, self.filename)
                if _applies_to(node, ImportChecker.targetted_modules[243]):
                    yield from _imr243(node)
                if _applies_to(node, ImportChecker.targetted_modules[244]):
                    yield from _imr244(node)
                if _applies_to(node, ImportChecker.targetted_modules[245]):
                    yield from _imr245(node)


ERROR_MESSAGES = {
    200: "Imports are only allowed on module level.",
    201: "Import aliases must be at least two characters long.",
    202: "Import alias has no effect.",
    220: "Missing import alias for non-trivial import.",
    221: "Multiple imports in one import statement.",
    222: "import statements are forbidden.",
    223: "import statements with alias must not contain duplicate module names.",
    240: "Multiple imports in one from-import statement.",
    241: "from-import statements must only import modules.",
    242: "from-import statements must not import modules.",
    243: "'import *' is forbidden.",
    244: "Relative imports are forbidden.",
    245: "from-import statements are forbidden.",
}

ERROR_HINTS = {
    200: "Move this import to the top of the file.",
    201: 'Choose a longer alias after the "as" keyword.',
    202: 'Remove the "as" keyword and following alias.',
    220: 'Use "as" keyword and provide a shorter alias.',
    221: "Split onto multiple lines.",
    222: 'Use "from" syntax instead.',
    223: 'Use "from" syntax instead or choose a different alias.',
    240: "Split onto multiple lines.",
    241: "Import the containing module instead.",
    242: "Import functions/classes directly instead.",
    243: "Import individual elements instead.",
    244: "Change the imported module to an absolute path.",
    245: 'Use the "import" syntax instead.',
}


def _error_tuple(error_code: int, node: ast.AST) -> Tuple[int, int, str, type]:
    return (
        node.lineno,
        node.col_offset,
        f"IMR{error_code} {ERROR_MESSAGES[error_code]} (hint: {ERROR_HINTS[error_code]})",
        ImportChecker,
    )


def _applies_to(
    node: Union[ast.Import, ast.ImportFrom],
    incexclude: Tuple[List[str], List[str]],
) -> bool:
    if isinstance(node, ast.Import):
        modules = [imp.name for imp in node.names]
    else:
        modules = [node.module]

    for module in modules:
        if not module:  # "from ." causes module to be None
            module = ""
        includes = any(
            fnmatch.fnmatch(module, target) for target in incexclude[0]
        )
        excludes = any(
            fnmatch.fnmatch(module, target) for target in incexclude[1]
        )
        if includes and not excludes:
            return True
    return False


def _imr200(
    node: Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef],
    incexclude: Tuple[List[str], List[str]],
) -> Iterable[Tuple[int, int, str, type]]:
    """
    Imports should only happen on module level, not locally.
    """
    for ancestor in ast.walk(node):
        if isinstance(ancestor, ast.Import) or isinstance(
            ancestor, ast.ImportFrom
        ):
            if _applies_to(ancestor, incexclude):
                yield _error_tuple(200, ancestor)


def _imr201(
    node: Union[ast.Import, ast.ImportFrom]
) -> Iterable[Tuple[int, int, str, type]]:
    """
    Alias identifiers defined from as segments should be at least two characters long.
    """
    for name in node.names:
        if name.asname and len(name.asname) == 1:
            yield _error_tuple(201, node)


def _imr202(
    node: Union[ast.Import, ast.ImportFrom]
) -> Iterable[Tuple[int, int, str, type]]:
    """
    Alias identifiers should not have the same name as the imported object.
    """
    for name in node.names:
        if name.name == name.asname:
            yield _error_tuple(202, node)


def _imr220(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, if the imported module is a submodule, i.e. not a top level module, an "as" segment should be present.
    """
    for name in node.names:
        if "." in name.name and not name.asname:
            yield _error_tuple(220, node)
            break


def _imr221(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, each import statement should only import one module.
    """
    if len(node.names) > 1:
        yield _error_tuple(221, node)


def _imr222(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    The import syntax should not be used.
    """
    yield _error_tuple(222, node)


def _imr223(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the `import` syntax, do not duplicate module names in the `as` segment.
    """
    for name in node.names:
        if name.name.split(".")[-1] == name.asname:
            yield _error_tuple(223, node)


def _imr240(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the "from" syntax, the import segment only contains one import.
    """
    if len(node.names) > 1:
        yield _error_tuple(240, node)


def _imr241(
    node: ast.ImportFrom, filename: str
) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the "from" syntax, only submodules are imported, not module elements.
    """
    for name in node.names:
        if not imports_submodule(
            filename, node.level, node.module or "", name.name
        ):
            yield _error_tuple(241, node)


def _imr242(
    node: ast.ImportFrom, filename: str
) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the "from" syntax, only module elements are imported, not submodules.
    """
    for name in node.names:
        if imports_submodule(
            filename, node.level, node.module or "", name.name
        ):
            yield _error_tuple(242, node)


def _imr243(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the "from" syntax, import * should not be used.
    """
    for name in node.names:
        if name.name == "*":
            yield _error_tuple(243, node)
            break


def _imr244(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    Relative imports should not be used.
    """
    if node.level != 0:
        yield _error_tuple(244, node)


def _imr245(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    The "from" syntax should not be used.
    """
    yield _error_tuple(245, node)
