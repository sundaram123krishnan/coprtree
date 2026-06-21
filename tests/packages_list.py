import json
from dataclasses import dataclass
from pathlib import Path

from coprtree.models import BuildEnv, BuildTarget

ROOT = Path(__file__).parent
PACKAGE_DATA = ROOT / "packages.json"


@dataclass(frozen=True)
class TestPackage:
    target: BuildTarget
    env: BuildEnv
    expected_levels: list[list[str]]


def load_packages() -> list[TestPackage]:
    return [
        TestPackage(
            target=BuildTarget(
                provider=p["provider"], name=p["name"], version=p.get("version")
            ),
            env=BuildEnv(chroot=p["chroot"], copr_project=p["copr_project"]),
            expected_levels=p["expected_levels"],
        )
        for p in json.loads(PACKAGE_DATA.read_text())["packages"]
    ]


PACKAGES = load_packages()
