"""
Test fedora repo checks
"""

import json
import subprocess

import pytest

from coprtree.constants import COPR_BASEURL
from coprtree.models import BuildEnv
from coprtree.providers import get_provider
from coprtree.repo_check import has_package_in_repository

from packages_list import ROOT

CHECKS = json.loads((ROOT / "packages.json").read_text())["repository_checks"]


def dnf_provides(capability: str, env: BuildEnv) -> bool:
    copr = COPR_BASEURL.format(project=env.copr_project, chroot=env.chroot)
    result = subprocess.run(
        [
            "dnf",
            "repoquery",
            "--quiet",
            "--whatprovides",
            capability,
            "--repofrompath",
            f"copr,{copr}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return bool(result.stdout.strip())


@pytest.mark.parametrize("case", CHECKS, ids=lambda c: f"{c['provider']}:{c['name']}")
def test_repo_check_matches_dnf(case):
    provider = get_provider(case["provider"])
    env = BuildEnv(chroot=case["chroot"], copr_project=case["copr_project"])
    capability = provider.provide(case["name"])
    app = has_package_in_repository(
        provider, case["name"], case.get("requirement", "0"), env
    )
    dnf = dnf_provides(capability, env)
    print(app)

    assert app == dnf, (
        f"{case['name']}: capability {capability!r} -> "
        f"app provided={app}, dnf provided={dnf}"
    )
