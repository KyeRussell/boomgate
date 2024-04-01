import dataclasses
from datetime import datetime
from ..vulnerabilities import Vulnerability
from typing import TypeVar, Generic


class Ecosystem:
    @classmethod
    def get_package(cls, package_name: str):
        raise NotImplementedError()


V = TypeVar("V", bound="Version")


@dataclasses.dataclass(slots=True)
class Package(Generic[V]):
    name: str
    versions: "dict[str, V]" = dataclasses.field(default_factory=dict)
    license: str | None = None
    homepage_url: str | None = None
    ecosystem_url: str | None = None
    description: str | None = None
    author_name: str | None = None
    author_email: str | None = None
    maintainer_name: str | None = None
    maintainer_email: str | None = None


R = TypeVar("R", bound="Release")


@dataclasses.dataclass(slots=True)
class Version(Generic[R]):
    number: str
    releases: "list[R]" = dataclasses.field(default_factory=list)
    vulnerabilities: list[Vulnerability] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(slots=True)
class Release:
    download_url: str | None = None
    uploaded_at: datetime | None = None
