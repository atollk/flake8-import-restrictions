from tests.util import BaseTest


class Test_I2044(BaseTest):
    def error_code(self) -> str:
        return "I2044"

    def test_pass_1(self):
        code = """
        import os
        from os import path
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        from .foo import bar
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "I2044", 1, 1)

    def test_fail_2(self):
        code = """
        from ..foo import bar
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "I2044", 1, 1)

    def test_fail_3(self):
        code = """
        from . import foo
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "I2044", 1, 1)
