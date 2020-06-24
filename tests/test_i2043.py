
from tests.util import BaseTest


class Test_I2043(BaseTest):
    def error_code(self) -> str:
        return "I2043"

    def test_pass_1(self):
        code = """
        import os
        from os import path, environ
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        from os import *
        """
        result = self.run_flake8(code, True)
        assert result != []

