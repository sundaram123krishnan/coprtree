"""
Test the fedora provide name
"""

import json

import pytest

from coprtree.providers import get_provider

from packages_list import ROOT

CAPABILITIES = json.loads((ROOT / "packages.json").read_text())["capabilities"]


@pytest.mark.parametrize(
    "case", CAPABILITIES, ids=lambda c: f"{c['provider']}:{c['name']}"
)
def test_provide(case):
    provider = get_provider(case["provider"])
    name = provider.normalize(case["name"])
    assert provider.provide(name) == case["capability"]


def test_cpan_version_constraints():
    cpan = get_provider("metacpan.org")
    assert cpan.version_constraints("0") == []  # "any version"
    assert cpan.version_constraints("5.17") == [(">=", "5.17")]  # bare = ">="
    assert cpan.version_constraints(">= 1.2, < 2.0") == [(">=", "1.2"), ("<", "2.0")]
    assert cpan.version_constraints("== 1.5") == [("=", "1.5")]
    assert cpan.version_constraints(">= 1.2, != 1.5, < 2.0") is None


def test_pypi_version_constraints():
    pypi = get_provider("pypi.org")
    assert pypi.version_constraints("") == []
    assert pypi.version_constraints("*") == []
    assert pypi.version_constraints(">=2.0") == [(">=", "2.0")]
    assert pypi.version_constraints("<2,>=1.6") == [("<", "2"), (">=", "1.6")]
    assert pypi.version_constraints("==2.0") == [("=", "2.0")]
    assert pypi.version_constraints("<2, >=1.6") == [("<", "2"), (">=", "1.6")]
    assert pypi.version_constraints("~=1.4") is None
    assert pypi.version_constraints("!=1.0") is None
    assert pypi.version_constraints("===1.0") is None
    assert pypi.version_constraints("==1.4.*") is None
