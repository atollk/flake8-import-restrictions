from tests.util import BaseTest


class Test_IMR223(BaseTest):
    def error_code(self) -> str:
        return "IMR223"

    def test_pass_1(self):
        code = """
        from os import path
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import os.path as ospath
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import os.path as path
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR223", 1, 1)
