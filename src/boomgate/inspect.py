from enum import Enum
import dataclasses
from .ecosystems.pypi import Package, PyPIVersion
from .vulnerabilities import Vulnerability
from typing import ClassVar
from collections import defaultdict
import abc


@dataclasses.dataclass(slots=True, kw_only=True)
class Risk(abc.ABC):
    name: ClassVar[str]
    name_plural: ClassVar[str | None] = None
    description: ClassVar[str]
    description_plural: ClassVar[str | None] = None
    description_format: ClassVar[str | None] = None

    @property
    def dynamic_description(self):
        if self.description_format:
            return self.description_format.format(self)
        return self.description

    @property
    def description_plural_list(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass(slots=True, kw_only=True)
class KnownVulnerability(Risk):
    name = "Known vulnerability"
    name_plural = "Known vulnerabilities"
    description = "A vulnerability is publicly known to exist in this package version."
    description_plural = (
        "Multiple vulnerabilities are publicly known to exist in this package version."
    )
    description_format = (
        "This package contains known vulnerability {self.vulnerability}."
    )
    vulnerability: Vulnerability

    @property
    def description_plural_list(self):
        return self.vulnerability.primary_identifier


@dataclasses.dataclass(slots=True, kw_only=True)
class NoSecurityPolicy(Risk):
    name = "No security policy"
    description = (
        "No security policy is provided by the package maintainers. This may make it "
        "harder for users to report vulnerabilities."
    )


class RiskTypes(Enum):
    KNOWN_VULNERABILITY = KnownVulnerability
    NO_SECURITY_POLICY = NoSecurityPolicy


# Create a type variable bound to class X


def inspect_package(package: Package, version: PyPIVersion):
    risks: dict[type[Risk], list[Risk]] = defaultdict(list)
    # Known vulnerabilities.
    for vulnerability in version.vulnerabilities:
        risks[KnownVulnerability].append(
            KnownVulnerability(vulnerability=vulnerability)
        )

    return risks
