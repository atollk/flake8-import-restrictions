from tests.util import BaseTest


class Test_IMR202(BaseTest):
    def error_code(self) -> str:
        return "IMR202"

    def test_pass_1(self):
        code = """
        import os
        from os import path
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import sys as sy
        from os import path as pat
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import os as os
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR202", 1, 1)

    def test_fail_2(self):
        code = """
        from os import environ as env, path as path
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR202", 1, 1)
