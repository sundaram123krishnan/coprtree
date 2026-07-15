"""
Distribution strategy tests (hermetic: no dnf, no network)
"""

import pytest

from coprtree.chroots import FEDORA, get_distribution, parse_chroot
from coprtree.exceptions import UnsupportedDistribution


def test_parse_chroot_splits_distro_release_arch():
    assert parse_chroot("fedora-44-x86_64") == ("fedora", "44", "x86_64")
    assert parse_chroot("fedora-rawhide-x86_64") == ("fedora", "rawhide", "x86_64")
    assert parse_chroot("centos-stream-9-x86_64") == ("centos-stream", "9", "x86_64")


@pytest.mark.parametrize(
    "chroot", ["garbage", "fedora-44", "-44-x86_64", "fedora--x86_64"]
)
def test_parse_chroot_rejects_malformed(chroot):
    with pytest.raises(UnsupportedDistribution):
        parse_chroot(chroot)


def test_get_distribution_unknown_raises():
    with pytest.raises(UnsupportedDistribution):
        get_distribution("debian")


def test_fedora_numbered_repos():
    repo_ids = [repo_id for repo_id, _ in FEDORA.repos("44", "x86_64")]
    assert repo_ids == ["fedora", "updates"]


def test_fedora_rawhide_has_no_updates():
    repo_ids = [repo_id for repo_id, _ in FEDORA.repos("rawhide", "x86_64")]
    assert repo_ids == ["fedora"]
