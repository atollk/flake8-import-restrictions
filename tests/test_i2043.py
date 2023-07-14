from tests.util import BaseTest


class Test_IMR243(BaseTest):
    def error_code(self) -> str:
        return "IMR243"

    def test_pass_1(self):
        code = """
        import os
        from os import path, environ
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        from os import *
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR243", 2, 1)
