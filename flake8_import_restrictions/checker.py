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
    2000,
    2001,
    2002,
    2020,
    2021,
    2022,
    2023,
    2040,
    2041,
    2042,
    2043,
    2044,
    2045,
}
DEFAULT_INCLUDE = {
    2000: ["*"],
    2001: ["*"],
    2002: ["*"],
    2021: ["*"],
    2023: ["*"],
    2041: ["*"],
    2043: ["*"],
}
DEFAULT_EXCLUDE = {2041: ["typing"]}


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
                f"--i{error}_include",
                type=str,
                comma_separated_list=True,
                default=DEFAULT_INCLUDE.get(error, []),
                parse_from_config=True,
                help=f"List of modules that I{error} is applied to. Allows UNIX wildcards.",
            )
            option_manager.add_option(
                f"--i{error}_exclude",
                type=str,
                comma_separated_list=True,
                default=DEFAULT_EXCLUDE.get(error, []),
                parse_from_config=True,
                help=f"List of modules that I{error} is *not* applied to. Overwrites the _include flag. Allows UNIX wildcards.",
            )

    @staticmethod
    def parse_options(
        option_manager: flake8.options.manager.OptionManager,
        options: argparse.Namespace,
        extra_args,
    ):
        for error in ALL_ERRORS:
            ImportChecker.targetted_modules[error] = (
                getattr(options, f"i{error}_include"),
                getattr(options, f"i{error}_exclude"),
            )

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.ClassDef)
                or isinstance(node, ast.FunctionDef)
                or isinstance(node, ast.AsyncFunctionDef)
            ):
                yield from _imr200(node, ImportChecker.targetted_modules[2000])

            if isinstance(node, ast.Import):
                if _applies_to(node, ImportChecker.targetted_modules[2001]):
                    yield from _imr201(node)
                if _applies_to(node, ImportChecker.targetted_modules[2002]):
                    yield from _imr202(node)
                if _applies_to(node, ImportChecker.targetted_modules[2020]):
                    yield from _imr220(node)
                if _applies_to(node, ImportChecker.targetted_modules[2021]):
                    yield from _imr221(node)
                if _applies_to(node, ImportChecker.targetted_modules[2022]):
                    yield from _imr222(node)
                if _applies_to(node, ImportChecker.targetted_modules[2023]):
                    yield from _imr223(node)

            if isinstance(node, ast.ImportFrom):
                if _applies_to(node, ImportChecker.targetted_modules[2001]):
                    yield from _imr201(node)
                if _applies_to(node, ImportChecker.targetted_modules[2002]):
                    yield from _imr202(node)
                if _applies_to(node, ImportChecker.targetted_modules[2040]):
                    yield from _imr240(node)
                if _applies_to(node, ImportChecker.targetted_modules[2041]):
                    yield from _imr241(node, self.filename)
                if _applies_to(node, ImportChecker.targetted_modules[2042]):
                    yield from _imr242(node, self.filename)
                if _applies_to(node, ImportChecker.targetted_modules[2043]):
                    yield from _imr243(node)
                if _applies_to(node, ImportChecker.targetted_modules[2044]):
                    yield from _imr244(node)
                if _applies_to(node, ImportChecker.targetted_modules[2045]):
                    yield from _imr245(node)


ERROR_MESSAGES = {
    2000: "Imports are only allowed on module level.",
    2001: "Import aliases must be at least two characters long.",
    2002: "Import alias has no effect.",
    2020: "Missing import alias for non-trivial import.",
    2021: "Multiple imports in one import statement.",
    2022: "import statements are forbidden.",
    2023: "import statements with alias must not contain duplicate module names.",
    2040: "Multiple imports in one from-import statement.",
    2041: "from-import statements must only import modules.",
    2042: "from-import statements must not import modules.",
    2043: "'import *' is forbidden.",
    2044: "Relative imports are forbidden.",
    2045: "from-import statements are forbidden.",
}

ERROR_HINTS = {
    2000: "Move this import to the top of the file.",
    2001: 'Choose a longer alias after the "as" keyword.',
    2002: 'Remove the "as" keyword and following alias.',
    2020: 'Use "as" keyword and provide a shorter alias.',
    2021: "Split onto multiple lines.",
    2022: 'Use "from" syntax instead.',
    2023: 'Use "from" syntax instead or choose a different alias.',
    2040: "Split onto multiple lines.",
    2041: "Import the containing module instead.",
    2042: "Import functions/classes directly instead.",
    2043: "Import individual elements instead.",
    2044: "Change the imported module to an absolute path.",
    2045: 'Use the "import" syntax instead.',
}


def _error_tuple(error_code: int, node: ast.AST) -> Tuple[int, int, str, type]:
    return (
        node.lineno,
        node.col_offset,
        f"I{error_code} {ERROR_MESSAGES[error_code]} (hint: {ERROR_HINTS[error_code]})",
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
                yield _error_tuple(2000, ancestor)


def _imr201(
    node: Union[ast.Import, ast.ImportFrom]
) -> Iterable[Tuple[int, int, str, type]]:
    """
    Alias identifiers defined from as segments should be at least two characters long.
    """
    for name in node.names:
        if name.asname and len(name.asname) == 1:
            yield _error_tuple(2001, node)


def _imr202(
    node: Union[ast.Import, ast.ImportFrom]
) -> Iterable[Tuple[int, int, str, type]]:
    """
    Alias identifiers should not have the same name as the imported object.
    """
    for name in node.names:
        if name.name == name.asname:
            yield _error_tuple(2002, node)


def _imr220(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, if the imported module is a submodule, i.e. not a top level module, an "as" segment should be present.
    """
    for name in node.names:
        if "." in name.name and not name.asname:
            yield _error_tuple(2020, node)
            break


def _imr221(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, each import statement should only import one module.
    """
    if len(node.names) > 1:
        yield _error_tuple(2021, node)


def _imr222(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    The import syntax should not be used.
    """
    yield _error_tuple(2022, node)


def _imr223(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the `import` syntax, do not duplicate module names in the `as` segment.
    """
    for name in node.names:
        if name.name.split(".")[-1] == name.asname:
            yield _error_tuple(2023, node)


def _imr240(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, the import segment only contains one import.
    """
    if len(node.names) > 1:
        yield _error_tuple(2040, node)


def _imr241(
    node: ast.ImportFrom, filename: str
) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, only submodules are imported, not module elements.
    """
    for name in node.names:
        if not imports_submodule(filename, node.level, node.module, name.name):
            yield _error_tuple(2041, node)


def _imr242(
    node: ast.ImportFrom, filename: str
) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, only module elements are imported, not submodules.
    """
    for name in node.names:
        if imports_submodule(filename, node.level, node.module, name.name):
            yield _error_tuple(2042, node)


def _imr243(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, import * should not be used.
    """
    for name in node.names:
        if name.name == "*":
            yield _error_tuple(2043, node)
            break


def _imr244(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    Relative imports should not be used.
    """
    if node.level != 0:
        yield _error_tuple(2044, node)


def _imr245(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    The from syntax should not be used.
    """
    yield _error_tuple(2045, node)
