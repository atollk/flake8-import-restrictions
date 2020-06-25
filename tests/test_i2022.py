from tests.util import BaseTest


class Test_I2022(BaseTest):
    def error_code(self) -> str:
        return "I2022"

    def test_pass_1(self):
        code = """
        from os import path
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        import os.path as path
        """
        result = self.run_flake8(code, True)
        assert result != []

    def test_fail_2(self):
        code = """
        import os
        """
        result = self.run_flake8(code, True)
        assert result != []
