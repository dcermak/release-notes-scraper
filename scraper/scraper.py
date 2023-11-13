from dataclasses import dataclass
import sys

import requests
from packaging.version import InvalidVersion, Version, parse


@dataclass
class Release:
    version: str
    changelog: str

    def __post_init__(self) -> None:
        self.changelog = self.changelog.replace("\r\n", "\n")

    def __str__(self) -> str:
        return f"""{self.version}:

{self.changelog}
"""


def fetch_releases(
    owner: str,
    repository: str,
    min_version: Version | None = None,
    max_version: Version | None = None,
) -> list[Release]:
    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repository}/releases?per_page=100"
    )

    releases: list[Release] = []

    for release in resp.json():
        VER_STR_KEYS = ("name", "tag_name")
        ver = None

        for ver_str_key in VER_STR_KEYS:
            ver_str = (release.get(ver_str_key, "") or "").replace("v", "").strip()
            try:
                ver = parse(ver_str)
                break
            except InvalidVersion:
                pass

        if ver is None:
            print(
                f"skipping version string {', '.join(release.get(k,'') for k in VER_STR_KEYS)},"
                " not a valid semver",
                file=sys.stderr,
            )
            continue

        assert isinstance(ver, Version)

        if min_version is not None and ver <= min_version:
            continue
        if max_version is not None and ver > max_version:
            continue

        releases.append(Release(version=str(ver), changelog=release["body"]))

    return releases


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Grab the release changelog from Github for a given repository and an optional version constraint"
    )

    parser.add_argument("owner", type=str, nargs=1, help="The github repository owner")
    parser.add_argument(
        "repository", type=str, nargs=1, help="The github repository name"
    )

    parser.add_argument(
        "--min-version",
        type=str,
        nargs=1,
        help="The minimum version that should *not* be included in the changelog",
        default=[None],
    )
    parser.add_argument(
        "--max-version",
        type=str,
        nargs=1,
        help="The maximum version that should be included in the changelog",
        default=[None],
    )

    args = parser.parse_args()

    min_version = None
    if args.min_version[0] is not None:
        min_version = parse(args.min_version[0])
    max_version = None
    if args.max_version[0] is not None:
        max_version = parse(args.max_version[0])

    if (
        min_version is not None
        and max_version is not None
        and min_version > max_version
    ):
        raise ValueError(
            f"minimal version {min_version} is larger than maximum version {max_version}"
        )

    for rel in fetch_releases(
        args.owner[0],
        args.repository[0],
        min_version,
        max_version,
    ):
        print(rel)
