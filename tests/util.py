import abc
import dataclasses
import re
import textwrap
from typing import List

import pytest


@dataclasses.dataclass
class ReportedMessage:
    file: str
    line: int
    col: int
    code: str
    message: str

    @staticmethod
    def from_raw(report: str):
        m = re.match(r"(.*?):(\d+):(\d+): ((?:\w|\d)+) (.*)", report)
        return ReportedMessage(m[1], int(m[2]), int(m[3]), m[4], m[5])


class BaseTest(abc.ABC):
    @abc.abstractmethod
    def error_code(self) -> str:
        raise NotImplementedError

    @pytest.fixture(autouse=True)
    def _flake8dir(self, flake8dir):
        self.flake8dir = flake8dir

    def run_flake8(self, code: str) -> List[ReportedMessage]:
        self.flake8dir.make_example_py(textwrap.dedent(code))
        result = self.flake8dir.run_flake8(
            extra_args=[f"--{self.error_code().lower()}_include=*"]
        )
        reports = [
            ReportedMessage.from_raw(report) for report in result.out_lines
        ]
        return [
            report for report in reports if report.code == self.error_code()
        ]

    def assert_error_at(
        self,
        reported_errors: List[ReportedMessage],
        error_code: str,
        line: int,
        col: int,
    ) -> None:
        error_found = any(
            report.line == line
            and report.col == col
            and report.code == error_code
            for report in reported_errors
        )
        if not error_found:
            pytest.fail(
                f"No error with code {error_code} at {line}:{col} found. Reported errors are: {reported_errors}"
            )
