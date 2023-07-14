from tests.util import BaseTest


class Test_IMR201(BaseTest):
    def error_code(self) -> str:
        return "IMR201"

    def test_pass_1(self):
        code = """
        import os
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        import os.path as pa
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_3(self):
        code = """
        from os.path import join as joi
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        import os as o
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR201", 2, 1)

    def test_fail_2(self):
        code = """
        from os import path as p
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "IMR201", 2, 1)
