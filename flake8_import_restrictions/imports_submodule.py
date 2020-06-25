import importlib
import sys
import types
import os.path
from typing import Optional


def imports_submodule(
    filename: str, level: int, from_: str, import_: str
) -> Optional[bool]:
    """
    Tests whether the statement "from from_ import import_" executed in the specified file
    loads a module or a module element.
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
    for include in sys.path:
        path_abs = os.path.abspath(path)
        include_abs = os.path.realpath(os.path.abspath(include))
        if os.path.commonpath([path_abs, include_abs]) == include_abs:
            return os.path.relpath(path_abs, include_abs)
