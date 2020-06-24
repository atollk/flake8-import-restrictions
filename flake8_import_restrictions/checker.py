import argparse
import ast
import importlib
from typing import Iterable, Tuple, Union, List, Dict

import flake8.options.manager


class ImportChecker:
    """
    A flake8 plugin used to disallow certain forms of imports.
    """

    name = "flake8-import-restrictions"
    version = "1.0"
    targetted_modules: Dict[int, List[str]] = {}

    def __init__(self, tree: ast.AST, filename: str):
        self.tree = tree
        self.filename = filename

    @staticmethod
    def add_options(option_manager: flake8.options.manager.OptionManager):
        option_manager.add_option(
            "--select_c20",
            type=str,
            comma_separated_list=True,
            default=[],
            parse_from_config=True,
            help="Error types to use. Default: %(default)s",
        )

    @staticmethod
    def parse_options(
        option_manager: flake8.options.manager.OptionManager,
        options: argparse.Namespace,
        extra_args,
    ):
        pass

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        yield from _i2000(self.tree, ImportChecker.targetted_modules[2000])

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                yield from _i2001(node, ImportChecker.targetted_modules[2001])
                yield from _i2020(node, ImportChecker.targetted_modules[2020])
                yield from _i2021(node, ImportChecker.targetted_modules[2021])
                yield from _i2022(node, ImportChecker.targetted_modules[2022])

            if isinstance(node, ast.ImportFrom):
                yield from _i2001(node, ImportChecker.targetted_modules[2001])
                yield from _i2040(node, ImportChecker.targetted_modules[2040])
                yield from _i2041(node, ImportChecker.targetted_modules[2041])
                yield from _i2042(node, ImportChecker.targetted_modules[2042])
                yield from _i2043(node, ImportChecker.targetted_modules[2043])
                yield from _i2044(node, ImportChecker.targetted_modules[2044])
                yield from _i2045(node, ImportChecker.targetted_modules[2045])


ERROR_MESSAGES = {
    2000: "Generators in comprehension expression are on the same line.",
    2001: "Different segments of a comprehension expression share a line.",
    2002: "Multiple filter segments within a single comprehension expression.",
    2003: "Multiline comprehension expression are forbidden.",
    2004: "Singleline comprehension expression are forbidden.",
    2020: "Different segments of a conditional expression share a line.",
    2021: "Conditional expression used for assignment not surrounded by parantheses.",
    2022: "Nested conditional expressions are forbidden.",
    2023: "Multiline conditional expression are forbidden.",
    2024: "Singleline conditional expression are forbidden.",
    2025: "Conditional expressions are forbidden.",
}


def _error_tuple(error_code: int, node: ast.AST) -> Tuple[int, int, str, type]:
    return (
        node.lineno,
        node.col_offset,
        f"C{error_code} {ERROR_MESSAGES[error_code]}",
        ImportChecker,
    )


def _imports_submodule(filename: str, from_: str, impport_: str) -> bool:
    """
    Tests whether the statement "from from_ import import_" executed in the specified file
    loads a module or a module element.
    """
    return False  # TODO


def _i2000(tree: ast.AST, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    Imports should only happen on module level, not locally.
    """
    if not isinstance(tree, ast.Module):
        raise TypeError("Given AST is not a module.")

    for top_level_object in tree.body:
        if isinstance(top_level_object, ast.Import) or isinstance(top_level_object, ast.ImportFrom):
            continue

        for node in ast.walk(top_level_object):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                yield _error_tuple(2000, node)

def _i2001(node: Union[ast.Import, ast.ImportFrom], targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    Alias identifiers defined from as segments should be at least two characters long.
    """
    for name in node.names:
        if name.asname and len(name.asname) == 1:
            yield _error_tuple(2001, node)

def _i2020(node: ast.Import, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, if the imported module is a submodule, i.e. not a top level module, an "as" segment
    should be present.
    """
    for name in node.names:
        if "." in name.name and not name.asname:
            return [_error_tuple(2020, node)]

def _i2021(node: ast.Import, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, each import statement should only import one module.
    """
    if len(node.names) > 1:
        yield _error_tuple(2021, node)

def _i2022(node: ast.Import, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    The import syntax should not be used.
    """
    yield _error_tuple(2022, node)

def _i2040(node: ast.ImportFrom, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, the import segment only contains one import.
    """
    if len(node.names) > 1:
        yield _error_tuple(2040, node)


def _i2041(node: ast.ImportFrom, filename: str, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, only submodules are imported, not module elements.
    """
    for name in node.names:
        if not _imports_submodule(filename, "."*node.level + node.module, name.name):
            yield _error_tuple(2041, node)

def _i2042(node: ast.ImportFrom, filename: str, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, only module elements are imported, not submodules.
    """
    for name in node.names:
        if _imports_submodule(filename, "."*node.level + node.module, name.name):
            yield _error_tuple(2041, node)

def _i2043(node: ast.ImportFrom, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, import * should not be used.
    """
    for name in node.names:
        if name.name == "*":
            return [_error_tuple(2043, node)]

def _i2044(node: ast.ImportFrom, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    Relative imports should not be used.
    """
    if node.level != 0:
        yield _error_tuple(2044, node)

def _i2045(node: ast.ImportFrom, targetted_modules: List[str]) -> Iterable[Tuple[int, int, str, type]]:
    """
    The from syntax should not be used.
    """
    yield _error_tuple(2045, node)
