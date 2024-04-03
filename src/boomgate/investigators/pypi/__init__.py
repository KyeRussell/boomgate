from typing import Any
from pathlib import Path
from .. import Investigator, FilenameRegex
import re
from typing import TypedDict
import dataclasses


class ParsedRequirementsLine(TypedDict):
    package: str
    operator: str
    version: str


@dataclasses.dataclass(kw_only=True)
class RequirementsFile(Investigator):
    from_file = FilenameRegex(r"^requirements(.+|).txt$")
    content: str

    @classmethod
    def create_from_file(cls, file: Path) -> "RequirementsFile":
        return cls(content=file.read_text())

    def investigate(self):
        parsed = self.parse_requirements_file(self.content)
        result = [PyPIRequirement.from_dict(line) for line in parsed]
        return {"packages": result}

    @staticmethod
    def parse_requirements_file(content: str) -> list[ParsedRequirementsLine]:
        lines = content.splitlines()
        results: list[ParsedRequirementsLine] = []
        for line in lines:
            match = re.match(
                r"^(?P<package>[^=<>]+)(?P<operator>[<=>]+)(?P<version>.+)$", line
            )
            if not match:
                raise ValueError(f"Invalid requirement line: {line}")
            results.append(match.groupdict())  # type: ignore
        return results


@dataclasses.dataclass
class PyPIRequirement(Investigator):
    package: "PyPIPackage"

    @classmethod
    def from_dict(cls, data: ParsedRequirementsLine):
        return cls(package=PyPIPackage(data["package"]))

    def investigate(self) -> Any:
        return super().investigate()


@dataclasses.dataclass
class PyPIPackage(Investigator):
    name: str

    def investigate(self) -> Any:
        return super().investigate()
