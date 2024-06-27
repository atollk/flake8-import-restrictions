import os.path

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
    # Check that the empty `from_` is handled correctly.
    # For the complete code to run, we need to check a not-yet imported module
    assert not imports_submodule(FILE1, 1, "", "not_existing_module")


def test_relative_2():
    assert imports_submodule(FILE2, 2, "resources.a", "c")
    assert not imports_submodule(FILE2, 2, "resources.b", "B")
    assert not imports_submodule(FILE3, 2, "b", "B")


def test_relative_3():
    assert imports_submodule(FILE3, 3, "resources.a", "c")
    assert not imports_submodule(FILE3, 3, "resources.b", "B")
