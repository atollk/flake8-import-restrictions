import os.path
import sys

from flake8_import_restrictions.imports_submodule import imports_submodule

FILE1 = __file__
FILE2 = os.path.join(os.path.dirname(__file__), "resources", "dummy.py")
FILE3 = os.path.join(os.path.dirname(__file__), "resources", "a", "x.py")


def test_absolute_1():
    assert imports_submodule(FILE1, 0, "os", "path")
    assert not imports_submodule(FILE1, 0, "os", "environ")
    assert not imports_submodule(FILE1, 0, "os.path", "join")


def test_absolute_2():
    assert imports_submodule(FILE1, 0, "tests.resources", "a")
    assert imports_submodule(FILE1, 0, "tests.resources", "b")
    assert not imports_submodule(FILE1, 0, "tests.resources.b", "B")
    assert not imports_submodule(FILE1, 0, "tests.resources.b", "C")


def test_relative_1():
    assert imports_submodule(FILE1, 1, "resources", "a")
    assert imports_submodule(FILE1, 1, "resources.a", "c")
    assert not imports_submodule(FILE1, 1, "resources.a.c", "C")
    assert imports_submodule(FILE2, 1, "a", "c")
    assert not imports_submodule(FILE2, 1, "a.c", "C")


def test_relative_2():
    assert imports_submodule(FILE2, 2, "resources.a", "c")
    assert not imports_submodule(FILE2, 2, "resources.b", "B")
    assert not imports_submodule(FILE3, 2, "b", "B")


def test_relative_3():
    assert imports_submodule(FILE3, 3, "resources.a", "c")
    assert not imports_submodule(FILE3, 3, "resources.b", "B")


def test_non_existant():
    assert not imports_submodule(FILE1, 1, "a", "DOESNOTEXIST")


def test_relative_empty_from():
    # Check that the empty `from_` is handled correctly.
    # There have been issues with the relative import level in the past, so we want to make sure, there are no
    # "relative import beyond top-level package" exceptions. Thus, we need to change the Python Path (which is set to
    # the current working directory by imports_submodule() internally) to be as close as possible to the (imaginative)
    # file which is checked (`filename`).
    old_sys_path = sys.path
    sys.path = []
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    try:
        # For the complete code to run, we need to check not-yet imported modules
        assert imports_submodule(FILE2, 1, "", "not_existing_module") is False
        assert imports_submodule(FILE2, 1, "", "d") is True
        assert imports_submodule(FILE2, 1, "", "d.B") is False

    finally:
        os.chdir(old_cwd)
        sys.path = old_sys_path
