from tests.util import BaseTest


class Test_IMR242(BaseTest):
    def error_code(self) -> str:
        return "IMR242"

    def test_pass_1(self):
        code = """
        import os.path as pat
        from os import environ
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        from os import environ as env
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        from os import path
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR242", 2, 1)

    def test_fail_2(self):
        code = """
        from os import environ, path
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR242", 2, 1)
