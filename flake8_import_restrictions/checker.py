import argparse
import ast
from typing import Iterable, Tuple, Union

import flake8.options.manager


class ImportChecker:
    """
    A flake8 plugin used to disallow certain forms of imports.
    """

    name = "flake8-import-restrictions"
    version = "1.0"

    def __init__(self, tree: ast.AST):
        self.tree = tree

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
        yield from _i2000(self.tree)

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                pass

            if isinstance(node, ast.ImportFrom):
                pass


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


def _i2000(tree: ast.AST) -> Iterable[Tuple[int, int, str, type]]:
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

def _i2001(node: Union[ast.Import, ast.ImportFrom]) -> Iterable[Tuple[int, int, str, type]]:
    """
    Alias identifiers defined from as segments should be at least two characters long.
    """
    pass

def _i2020(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, if the imported module is a submodule, i.e. not a top level module, an as segment should be present.
    """
    pass

def _i2021(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the import syntax, each import statement should only import one module.
    """
    pass

def _i2022(node: ast.Import) -> Iterable[Tuple[int, int, str, type]]:
    """
    The import syntax should not be used.
    """
    pass

def _i2040(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, the import segment only contains one import.
    """
    pass

def _i2041(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, only submodules are imported, not module elements.
    """

def _i2042(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, only module elements are imported, not submodules.
    """
    pass

def _i2043(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    When using the from syntax, import * should not be used.
    """
    pass

def _i2044(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    Relative imports should not be used.
    """
    pass

def _i2045(node: ast.ImportFrom) -> Iterable[Tuple[int, int, str, type]]:
    """
    The from syntax should not be used.
    """
    pass
