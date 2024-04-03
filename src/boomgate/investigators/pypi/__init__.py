from typing import Any, Annotated
from pathlib import Path
from .. import Investigator, FilenameRegex
import re


class PyPI(Investigator):
    def investigate(
        self, input: Annotated[Path, FilenameRegex(r"^requirements(.+|).txt$")]
    ) -> Any:
        contents = input.read_text()
        self.parse_requirements_file(contents)

    @staticmethod
    def parse_requirements_file(requirements_file: str) -> Any:
        # dummy implementation
        lines = requirements_file.splitlines()
        results = []
        for line in lines:
            match = re.match(
                r"^(?P<package>[^=<>]+)(?P<operator>[<=>]+)(?P<version>.+)$", line
            )
            if not match:
                raise ValueError(f"Invalid requirement line: {line}")
            results.append(match.groupdict())
        return results
