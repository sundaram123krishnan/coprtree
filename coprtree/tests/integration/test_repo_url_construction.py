"""
Live reachability checks for each chroot's own repos().
"""

from collections.abc import Generator

import pytest

from coprtree.chroots import DISTRIBUTIONS
from coprtree.chroots.base import CPU_ARCH, Chroot
from coprtree.exceptions import UnsupportedDistribution
from coprtree.singleton import get_httpx_client

chroots: list[Chroot] = []

for cpu_arch in CPU_ARCH | {"i586"}:
    for distribution in DISTRIBUTIONS:
        releases = distribution.releases or (None,)
        for release in releases:
            try:
                chroots.append(distribution(arch=cpu_arch, release=release))
            except UnsupportedDistribution:
                continue


def _repo_urls(chroot: Chroot) -> Generator[str]:
    for _, kwargs in chroot.repos():
        for value in kwargs.values():
            yield from value if isinstance(value, list) else [value]


@pytest.mark.parametrize("chroot", chroots, ids=str)
def test_chroot_repo_urls_resolve(chroot: Chroot):
    """Every URL a chroot's repos() advertises actually responds 200."""
    client = get_httpx_client()
    for url in _repo_urls(chroot):
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200, f"{chroot}: {url} -> {response.status_code}"
