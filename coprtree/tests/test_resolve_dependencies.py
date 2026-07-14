"""
Test the resolver with the expected packages
"""

import pytest

from coprtree.coprtree import resolve_dependencies

from .packages_list import PACKAGES


@pytest.mark.parametrize("pkg", PACKAGES, ids=lambda p: p.target.name)
def test_resolve_dependencies(pkg):
    levels = resolve_dependencies(pkg.target, pkg.env)
    actual = [[node.name for node in level] for level in levels]
    assert actual == pkg.expected_levels
