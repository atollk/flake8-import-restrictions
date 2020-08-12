from tests.util import BaseTest


class Test_I2000(BaseTest):
    def error_code(self) -> str:
        return "I2000"

    def test_pass_1(self):
        code = """
        import os
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        from os import *
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_3(self):
        code = """
        if True:
            import os
        else:
            try:
                import sys
            except ImportError:
                pass
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        class X:
            import os
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "I2000", 2, 5)

    def test_fail_2(self):
        code = """
        def x():
            import os
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "I2000", 2, 5)
