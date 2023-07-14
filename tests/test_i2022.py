from tests.util import BaseTest


class Test_IMR222(BaseTest):
    def error_code(self) -> str:
        return "IMR222"

    def test_pass_1(self):
        code = """
        from os import path
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import os.path as path
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR222", 1, 1)

    def test_fail_2(self):
        code = """
        import os
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR222", 1, 1)
