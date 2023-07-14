from tests.util import BaseTest


class Test_IMR241(BaseTest):
    def error_code(self) -> str:
        return "IMR241"

    def test_pass_1(self):
        code = """
        import os.path as pat
        from os import path
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        from os import path as pat
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        from os.path import join
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR241", 1, 1)

    def test_fail_2(self):
        code = """
        from os import path, environ
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR241", 1, 1)
