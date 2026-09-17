"""
Opensuse Leap chroot tests
"""

# pylint: disable=protected-access

import pytest

from coprtree.chroots import get_chroot
from coprtree.chroots.base import CPU_ARCH
from coprtree.chroots.opensuse_leap import OpensuseLeap
from coprtree.constants import OPENSUSE_LEAP_METALINK
from coprtree.exceptions import UnsupportedDistribution

ALL_RELEASES = ("16.0",)
ALL_ARCHES = sorted(CPU_ARCH)


# ---------------------------------------------------------------------------
# __init__ / validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("release", ALL_RELEASES)
def test_init_accepts_every_known_release(release):
    """Every known release constructs fine."""
    leap = OpensuseLeap(release, "x86_64")
    assert leap.release == release
    assert leap.arch == "x86_64"


@pytest.mark.parametrize("arch", ALL_ARCHES)
def test_init_accepts_every_known_arch(arch):
    """Every known arch constructs fine."""
    leap = OpensuseLeap("16.0", arch)
    assert leap.arch == arch


def test_init_rejects_unknown_release():
    """Unknown release raises."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        OpensuseLeap("15.6", "x86_64")


def test_init_rejects_empty_release():
    """Empty release raises too."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        OpensuseLeap("", "x86_64")


def test_init_rejects_unknown_arch():
    """Unknown arch raises."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        OpensuseLeap("16.0", "riscv64")


def test_init_rejects_empty_arch():
    """Empty arch raises too."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        OpensuseLeap("16.0", "")


def test_init_checks_arch_before_release():
    """Both invalid at once - arch's error wins, since it's checked first."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        OpensuseLeap("15.6", "riscv64")


def test_init_error_message_names_the_distro_and_known_releases():
    """Bad-release error names opensuse-leap, the bad value, and what's known."""
    with pytest.raises(UnsupportedDistribution) as exc_info:
        OpensuseLeap("15.6", "x86_64")
    message = str(exc_info.value)
    assert "opensuse-leap" in message
    assert "15.6" in message
    assert repr(ALL_RELEASES) in message or str(ALL_RELEASES) in message


def test_init_error_message_names_known_arches():
    """Bad-arch error names the bad value and every known arch."""
    with pytest.raises(UnsupportedDistribution) as exc_info:
        OpensuseLeap("16.0", "riscv64")
    message = str(exc_info.value)
    assert "riscv64" in message
    for arch in ALL_ARCHES:
        assert arch in message


# ---------------------------------------------------------------------------
# _match — pure shape recognition, no validation
# ---------------------------------------------------------------------------


def test_match_extracts_release_and_arch():
    """Splits a well-shaped chroot string into (release, arch)."""
    assert OpensuseLeap._match("opensuse-leap-16.0-x86_64") == ("16.0", "x86_64")


def test_match_extracts_even_an_unknown_release():
    """_match only checks shape, not whether the values are actually valid."""
    assert OpensuseLeap._match("opensuse-leap-15.6-x86_64") == ("15.6", "x86_64")
    assert OpensuseLeap._match("opensuse-leap-16.0-riscv64") == ("16.0", "riscv64")


@pytest.mark.parametrize(
    "chroot",
    [
        "garbage",
        "",
        "opensuse",
        "opensuse-leap",
        "opensuse-leap-16.0",
        "opensuse-leap-16.0-x86_64-extra",
        "-leap-16.0-x86_64",
        "debian-12-x86_64",
        "fedora-44-x86_64",
        "opensuse-tumbleweed-x86_64",
        "Opensuse-Leap-16.0-x86_64",  # case-sensitive
        "opensuse-Leap-16.0-x86_64",
    ],
)
def test_match_rejects_wrong_shape(chroot):
    """Anything not shaped like opensuse-leap-X-Y comes back None."""
    assert OpensuseLeap._match(chroot) is None


def test_match_accepts_empty_release_segment_as_a_shape_match():
    """An empty release segment still counts as a shape match."""
    # "opensuse-leap--x86_64" still has 4 parts and starts with
    # "opensuse-leap", so shape-wise it matches; the empty release itself
    # is a semantic question for __init__/parse, not _match
    assert OpensuseLeap._match("opensuse-leap--x86_64") == ("", "x86_64")


# ---------------------------------------------------------------------------
# parse — shape mismatch -> None, shape match but invalid value -> raises
# ---------------------------------------------------------------------------


def test_parse_returns_instance_for_valid_chroot():
    """A valid chroot string gives back a real OpensuseLeap instance."""
    leap = OpensuseLeap.parse("opensuse-leap-16.0-x86_64")
    assert isinstance(leap, OpensuseLeap)
    assert leap.release == "16.0"
    assert leap.arch == "x86_64"


def test_parse_returns_none_for_malformed_shape():
    """A malformed shape gives back None, not an instance."""
    assert OpensuseLeap.parse("garbage") is None
    assert OpensuseLeap.parse("fedora-44-x86_64") is None
    assert OpensuseLeap.parse("opensuse-leap-16.0") is None


def test_parse_raises_not_none_for_shape_match_but_bad_release():
    """Shape matches but the release is bad - raises, doesn't quietly return None."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        OpensuseLeap.parse("opensuse-leap-15.6-x86_64")


def test_parse_raises_not_none_for_shape_match_but_bad_arch():
    """Shape matches but the arch is bad - raises, doesn't quietly return None."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        OpensuseLeap.parse("opensuse-leap-16.0-riscv64")


def test_parse_raises_for_empty_release_segment():
    """The empty-release edge case ends up raising too, end to end."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        OpensuseLeap.parse("opensuse-leap--x86_64")


# ---------------------------------------------------------------------------
# repos
# ---------------------------------------------------------------------------


def test_repos_has_a_single_oss_repo():
    """Leap only ever has the one opensuse-leap repo."""
    repos = OpensuseLeap("16.0", "x86_64").repos()
    ids = [repo_id for repo_id, _ in repos]
    assert ids == ["opensuse-leap"]


def test_repos_metalink_url_is_correctly_formatted():
    """Metalink URL matches the real template, not a hardcoded string."""
    leap = OpensuseLeap("16.0", "x86_64")
    repos = dict(leap.repos())
    assert repos["opensuse-leap"]["metalink"] == OPENSUSE_LEAP_METALINK.format(
        release="16.0", arch="x86_64"
    )


@pytest.mark.parametrize("arch", ALL_ARCHES)
def test_repos_metalink_is_arch_independent(arch):
    """Leap's oss tree is combined-arch - the metalink URL doesn't vary by arch."""
    repos = dict(OpensuseLeap("16.0", arch).repos())
    x86_64_repos = dict(OpensuseLeap("16.0", "x86_64").repos())
    assert (
        repos["opensuse-leap"]["metalink"] == x86_64_repos["opensuse-leap"]["metalink"]
    )


def test_repos_are_recomputed_not_accumulated():
    """Calling repos() twice doesn't pile up duplicate entries."""
    leap = OpensuseLeap("16.0", "x86_64")
    first = leap.repos()
    second = leap.repos()
    assert first == second
    assert first is not second


# ---------------------------------------------------------------------------
# __str__ (inherited from Chroot, only exercisable via a concrete subclass)
# ---------------------------------------------------------------------------


def test_str_format():
    """str() gives back the canonical distro-release-arch form."""
    assert str(OpensuseLeap("16.0", "x86_64")) == "opensuse-leap-16.0-x86_64"


def test_str_round_trips_through_get_chroot():
    """str() and get_chroot() are inverses of each other."""
    original = OpensuseLeap("16.0", "x86_64")
    reconstructed = get_chroot(str(original))
    assert reconstructed.release == original.release
    assert reconstructed.arch == original.arch


# ---------------------------------------------------------------------------
# get_chroot dispatch (package-level entrypoint most of the codebase uses)
# ---------------------------------------------------------------------------


def test_get_chroot_dispatches_to_opensuse_leap():
    """An opensuse-leap-shaped chroot string routes to an OpensuseLeap instance."""
    assert isinstance(get_chroot("opensuse-leap-16.0-x86_64"), OpensuseLeap)


def test_get_chroot_surfaces_leaps_own_validation_error():
    """Leap's own release error isn't swallowed into the generic one."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        _ = get_chroot("opensuse-leap-15.6-x86_64")
