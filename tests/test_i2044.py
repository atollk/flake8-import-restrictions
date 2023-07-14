from tests.util import BaseTest


class Test_IMR244(BaseTest):
    def error_code(self) -> str:
        return "IMR244"

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
        self.assert_error_at(result, "IMR244", 1, 1)

    def test_fail_2(self):
        code = """
        from ..foo import bar
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR244", 1, 1)

    def test_fail_3(self):
        code = """
        from . import foo
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR244", 1, 1)
