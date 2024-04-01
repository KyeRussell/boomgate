from . import Ecosystem, Package, Version, Release
import dataclasses
from datetime import datetime
from .. import cached_http
from ..vulnerabilities import Vulnerability, IdentifierType
import httpx


@dataclasses.dataclass(slots=True)
class PyPIPackage(Package["PyPIVersion"]):
    pass


@dataclasses.dataclass(slots=True)
class PyPIVersion(Version["PyPIRelease"]):
    pass


@dataclasses.dataclass(slots=True)
class PyPIRelease(Release):
    pass


class PyPI(Ecosystem):
    @classmethod
    def get_package(cls, package_name: str) -> PyPIPackage:
        response: httpx.Response = cached_http.get(
            f"https://pypi.org/pypi/{package_name}/json"
        )
        response.raise_for_status()
        response_json = response.json()

        # Build Package.
        package = PyPIPackage(
            name=package_name,
            license=response_json["info"]["license"],
            homepage_url=response_json["info"]["home_page"],
            ecosystem_url=f"https://pypi.org/project/{package_name}",
            description=response_json["info"]["summary"],
            author_name=response_json["info"]["author"],
            author_email=response_json["info"]["author_email"],
            maintainer_name=response_json["info"]["maintainer"],
            maintainer_email=response_json["info"]["maintainer_email"],
        )

        # Pull extended info for each PyPI Release, to build child Versions and Releases
        for version_number, version_releases in response_json["releases"].items():
            response = cached_http.get(
                f"https://pypi.org/pypi/{package_name}/{version_number}/json"
            )
            response.raise_for_status()
            response_json = response.json()

            version = PyPIVersion(number=version_number)

            # Vulnerabilities.
            for vulnerability in response_json["vulnerabilities"]:
                version.vulnerabilities.append(
                    Vulnerability(
                        primary_identifier=vulnerability["id"],
                        primary_identifier_type=IdentifierType.PYSEC,
                        summary=vulnerability["summary"],
                        details=vulnerability["details"],
                        url=vulnerability["link"],
                    )
                )

            for release in version_releases:
                version.releases.append(
                    PyPIRelease(
                        download_url=release["url"],
                        uploaded_at=datetime.fromisoformat(
                            release["upload_time_iso_8601"]
                        ),
                    )
                )

            package.versions[version_number] = version

        return package
