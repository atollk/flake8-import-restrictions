from tests.util import BaseTest


class Test_I2020(BaseTest):
    def error_code(self) -> str:
        return "I2020"

    def test_pass_1(self):
        code = """
        import os
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import os.path as path
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import os.path
        """
        result = self.run_flake8(code)
        assert result != []
