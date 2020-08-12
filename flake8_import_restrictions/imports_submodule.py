import importlib
import os.path
import sys
import types
from typing import Optional


def imports_submodule(
    filename: str, level: int, from_: str, import_: str
) -> Optional[bool]:
    """
    Tests whether the statement "from from_ import import_" executed in the specified file
    loads a module or a module element.

    :param filename The file from which the import statement is executed. Relevant for relative imports.
    :param level The "level", as specified by ast.FromImport nodes.
    :param from_ The module name in the "from" part of the statement.
    :param import_ The module or element name in the "import" part of the statement.
    :return None, if an error occurs, e.g. the given file is not part of any directory in sys.path. Otherwise,
    a bool is returned that is True if and only if the imported object is a module.
    """
    if level > 0:
        try:
            filename = os.path.dirname(_rel_to_sys_path(filename))
        except TypeError:
            return None
        package = ".".join(filename.split(os.path.sep))
    else:
        package = None

    try:
        parent = importlib.import_module("." * level + from_, package)
    except ImportError:
        return None
    if not hasattr(parent, import_):
        try:
            importlib.import_module(
                "." * level + from_ + "." + import_, package
            )
        except ImportError:
            return False
    return isinstance(getattr(parent, import_), types.ModuleType)


def _rel_to_sys_path(path: str) -> str:
    """Given an arbitrary filename, returns the equivalent relative path from the sys.path-directory it is contained in."""
    for include in sys.path:
        path_abs = os.path.abspath(path)
        include_abs = os.path.realpath(os.path.abspath(include))
        try:
            contained_in_include = (
                os.path.commonpath([path_abs, include_abs]) == include_abs
            )
        except ValueError:  # Can happen on Windows systems.
            contained_in_include = False
        if contained_in_include:
            return os.path.relpath(path_abs, include_abs)
