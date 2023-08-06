import dateutil.parser
import json
import pkgutil
import re

from packaging.specifiers import Version
from packaging.version import parse
from typing import Any, Dict, List, Union, Sequence, Tuple

from ochrona.client import pypi_fetch

PEP_SUPPORTED_OPERATORS = r"==|>=|<=|!=|~=|<|>"
INVALID_SPEC_CHARACTERS = r"\'|\"|\\|\/|\[|\]|\{|\}"

# License data from SPDX with additional Aliases added to map back
# Non-complaint license names to SPDX specification License IDs
LICENSE_DATA = json.loads(pkgutil.get_data(__name__, "../schema/spdx_modified.json"))  # type: ignore[arg-type]


class Dependency:
    """
    A python dependency object.

    Internal variables with `_reserved_` prefix are used for policy evaluation.
    """

    _raw: str = ""
    _reserved_name: str = ""
    _version: str = ""
    _version_major: str = ""
    _version_minor: str = ""
    _version_release: str = ""
    _operator: str = ""
    _full: str = ""
    _reserved_latest_version: str = ""
    _reserved_license_type: str = ""
    _reserved_latest_update: str = ""
    _reserved_release_count: str = ""
    _specified_hashes: Dict[str, List[str]] = {}
    _purl: str = ""
    _url: str = ""
    _summary: str = ""

    def __init__(self, dependency: Dict[str, Union[str, List[str]]]):
        version = dependency.get("version")
        if version is not None and isinstance(version, str):
            self._raw = self._clean(version.split(",")[0])
        parts = re.split(PEP_SUPPORTED_OPERATORS, self._raw)
        if len(parts) == 1:
            if "txt" in parts[0] and "-r" in parts[0]:
                self.is_reference = True
                return
            self._reserved_name = parts[0]
        elif len(parts) > 1:
            self._reserved_name = parts[0]
            self._parse_version(parts[1])
            self._operator = re.sub("[a-zA-Z0-9.-]", "", self._raw)  # TODO fix
        (
            self._reserved_latest_version,
            self._reserved_license_type,
            self._reserved_latest_update,
            self._reserved_release_count,
            self._summary,
        ) = self._pypi_details()
        self._full = self._provided_or_most_recent() or self._raw
        self._purl = f"pkg:pypi/{self._reserved_name}@{self._version}"
        hashes = dependency.get("hashes", [])
        if isinstance(hashes, List):
            self._parse_hashes(hash_list=hashes)
        self._url = f"https://pypi.org/pypi/{self._reserved_name}"

    def _parse_version(self, version: str):
        v = Version(version)
        self._version = v.base_version
        version_parts = v.release
        if len(version_parts) == 1:
            self._version_major = str(version_parts[0])
        elif len(version_parts) == 2:
            self._version_major = str(version_parts[0])
            self._version_minor = str(version_parts[1])
        else:
            self._version_major = str(version_parts[0])
            self._version_minor = str(version_parts[1])
            self._version_release = str(version_parts[2])

    def _pypi_details(self) -> Tuple[str, str, str, str, str]:
        """
        Calls to pypi to resolve transitive dependencies.
        """
        json_value = pypi_fetch(self._reserved_name)
        if json_value:
            latest_version = self._parse_latest_version(json_value)
            license_value = self._get_license(json_value)
            latest_release_date = self._parse_latest_update(json_value, latest_version)
            release_count = self._parse_release_count(json_value)
            summary = self._parse_summary(json_value)
            return (
                latest_version,
                license_value,
                latest_release_date,
                release_count,
                summary,
            )
        return "", "Unknown", "", "", ""

    def to_json(self) -> Dict[str, Any]:
        """
        Returns PythonDependency as a dict so it can be json deserialized.
        """
        return self.__dict__

    def _parse_latest_version(self, resp: Dict[str, Any]) -> str:
        version = resp.get("info", {}).get("version")
        if version is not None:
            return version
        # Fallback and check releases
        releases = resp.get("releases", {})
        if len(releases) > 1:
            return list(releases.keys())[-1]
        return ""

    def _parse_latest_update(self, resp: Dict[str, Any], latest_version: str) -> str:
        """
        Return when the latest version was published
        """
        latest_release = resp.get("releases", {}).get(latest_version)
        if latest_release is not None and isinstance(latest_release, list):
            release_artifact_dates = []
            for artifact in latest_release:
                try:
                    upload_time = artifact.get("upload_time_iso_8601")
                    parsed_upload_time = dateutil.parser.isoparse(upload_time)
                    release_artifact_dates.append(parsed_upload_time)
                except Exception:
                    pass
            latest_artifact_timestamp = max(release_artifact_dates)
            return latest_artifact_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        return ""

    def _parse_release_count(self, resp: Dict[str, Any]) -> str:
        """
        Returns the total number of releases
        """
        return f"{len(resp.get('releases', []))}"

    def _get_license(self, resp: Dict[str, Any]) -> str:
        # Check License field first
        raw_license = resp.get("info", {}).get("license", None)
        if raw_license is not None and raw_license.strip() != "":
            for ltype in LICENSE_DATA.get("licenses"):
                if raw_license in ltype.get("aliases"):
                    return ltype.get("licenseId")
            return raw_license
        else:
            # Fall back to Classifiers
            classifiers = resp.get("info", {}).get("classifiers", [])
            for c in classifiers:
                if "License" in c:
                    cleaned = c.replace("License :: OSI Approved ::", "").strip()
                    for ltype in LICENSE_DATA.get("licenses"):
                        if cleaned in ltype.get("aliases"):
                            return ltype.get("licenseId")
                    return cleaned
        return "Unknown"

    def _parse_hashes(self, hash_list: List[str]):
        hash_dict: Dict[str, List[str]] = {}
        for h in hash_list:
            parts = h.split(":")
            if parts[0] in hash_dict:
                hash_dict[parts[0]].append(parts[1])
            else:
                hash_dict[parts[0]] = [parts[1]]
        self._specified_hashes = hash_dict

    def _parse_summary(self, resp: Dict[str, Any]) -> str:
        return resp.get("info", {}).get("summary", "None")

    def _provided_or_most_recent(self) -> str:
        """
        During resolution we should decide if the provided dependency, or the
        most recent version of the dependency should be returned.

        ex.
            Required if pkg>=1.0.1
            Current version is pkg==1.2.4
            We should return pkg==1.2.4
        """
        if self._operator == ">=" and parse(self._version) <= parse(
            self._reserved_latest_version
        ):
            return f"{self._reserved_name}=={self._reserved_latest_version}"
        elif (
            self._operator == ""
            and self._version == ""
            and self._reserved_latest_version != ""
        ):
            return f"{self._reserved_name}=={self._reserved_latest_version}"
        return self._raw

    def _clean(self, raw: str) -> str:
        return re.sub(INVALID_SPEC_CHARACTERS, "", raw)

    @property
    def full(self) -> str:
        return self._full

    @property
    def license_type(self) -> str:
        return self._reserved_license_type

    @property
    def name(self) -> str:
        return self._reserved_name

    @property
    def version(self) -> str:
        return self._version

    @property
    def purl(self) -> str:
        return self._purl

    @property
    def hashes(self) -> Dict[str, List[str]]:
        return self._specified_hashes

    @property
    def url(self) -> str:
        return self._url

    @property
    def summary(self) -> str:
        return self._summary
