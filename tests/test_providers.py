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
def test_fedora_provide(case):
    provider = get_provider(case["provider"])
    assert provider.fedora_provide(case["name"]) == case["capability"]
