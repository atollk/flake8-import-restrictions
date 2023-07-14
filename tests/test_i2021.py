from tests.util import BaseTest


class Test_IMR221(BaseTest):
    def error_code(self) -> str:
        return "IMR221"

    def test_pass_1(self):
        code = """
        import os
        import sys as sy
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        from os import path, environ
        import sys
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import os, sys
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR221", 1, 1)

    def test_fail_2(self):
        code = """
        import curses.ascii, curses.panel
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR221", 1, 1)
