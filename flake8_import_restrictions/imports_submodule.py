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
    old_sys_path = sys.path
    try:
        sys.path += [os.getcwd()]
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
        except (ImportError, TypeError):
            return None
        if not hasattr(parent, import_):
            try:
                importlib.import_module(
                    "." * level + (from_ + "." if from_ else "") + import_,
                    package,
                )
            except ImportError:
                return False
            except ValueError:  # only relevant for Python 3.8
                if sys.version_info[1] <= 8:
                    return False
                else:
                    raise
        return isinstance(getattr(parent, import_), types.ModuleType)
    finally:
        sys.path = old_sys_path


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
