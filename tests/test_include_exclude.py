import textwrap
from typing import List

import pytest

from tests.util import ReportedMessage


class Test_IncludeExclude:
    @pytest.fixture(autouse=True)
    def _flake8dir(self, flake8_path):
        self.flake8_path = flake8_path

    def run_flake8(
        self, code: str, include: List[str], exclude: List[str]
    ) -> List[ReportedMessage]:
        (self.flake8_path / "example.py").write_text(textwrap.dedent(code))
        args = [
            f"--imr222_include={','.join(include)}",
            f"--imr222_exclude={','.join(exclude)}",
            "--select=IMR",
        ]
        result = self.flake8_path.run_flake8(args)
        reports = [ReportedMessage.from_raw(report) for report in result.out_lines]
        return [report for report in reports if report.code == "IMR222"]

    def test_1(self):
        code = "import os"
        result = self.run_flake8(code, ["*"], [])
        assert result != []

    def test_2(self):
        code = "import os"
        result = self.run_flake8(code, ["*"], ["os"])
        assert result == []

    def test_3(self):
        code = "import os.path"
        result = self.run_flake8(code, ["os.*"], [])
        assert result != []

    def test_4(self):
        code = "import os.path"
        result = self.run_flake8(code, ["os.*"], ["os.path"])
        assert result == []

    def test_5(self):
        code = "import os.path"
        result = self.run_flake8(code, ["os.path"], ["*"])
        assert result == []
