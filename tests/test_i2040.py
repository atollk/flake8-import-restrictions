from tests.util import BaseTest


class Test_I2040(BaseTest):
    def error_code(self) -> str:
        return "I2040"

    def test_pass_1(self):
        code = """
        import os
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        from os import path
        from os import environ
        from xml import etree
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        from os import path, environ
        """
        result = self.run_flake8(code)
        assert result != []

    def test_fail_2(self):
        code = """
        from curses import ascii, panel
        """
        result = self.run_flake8(code)
        assert result != []
