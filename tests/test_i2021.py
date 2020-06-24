
from tests.util import BaseTest


class Test_I2021(BaseTest):
    def error_code(self) -> str:
        return "I2021"

    def test_pass_1(self):
        code = """
        import os
        import sys as sy
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        from os import path, environ
        import sys
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        import os, sys
        """
        result = self.run_flake8(code, True)
        assert result != []

    def test_fail_2(self):
        code = """
        import curses.ascii, curses.panel
        """
        result = self.run_flake8(code, True)
        assert result != []
