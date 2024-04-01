import dataclasses
from enum import Enum
from datetime import datetime
import re


class IdentifierType(str, Enum):
    CVE = {"name": "CVE", "regex": re.compile(r"^CVE-\d{4}-\d+$")}
    PYSEC = {"name": "PySec", "regex": re.compile(r"^PYSEC-\d{4}-\d+$")}
    GHSA = {
        "name": "GitHub Security Advisory",
        "regex": re.compile(r"^GHSA-\w+-\w+-\w+$"),
    }


class UnknownIdentifierError(Exception):
    pass


class IdentifierAlreadyExistsError(Exception):
    pass


@dataclasses.dataclass(slots=True)
class Vulnerability:
    primary_identifier: str
    primary_identifier_type: IdentifierType
    identifiers: dict[IdentifierType, str] = dataclasses.field(default_factory=dict)
    summary: str | None = None
    details: str | None = None
    url: str | None = None
    fixed_in: list[str] | None = None
    withdrawn_at: datetime | None = None

    @property
    def has_been_withdrawn(self):
        return self.withdrawn_at is not None

    def add_identifier(self, identifier: str):
        """Add a new identifier, detecting the type automatically."""
        for identifier_type in IdentifierType:
            if identifier_type.value["regex"].match(identifier):
                if (
                    identifier_type in self.identifiers
                    and self.identifiers[identifier_type] != identifier
                ):
                    raise IdentifierAlreadyExistsError()
                self.identifiers[identifier_type] = identifier
                return
        raise UnknownIdentifierError()
