"""
Opensuse Tumbleweed chroot tests
"""

# pylint: disable=protected-access

import pytest
from coprtree.chroots import get_chroot
from coprtree.chroots.opensuse_leap import OpensuseLeap
from coprtree.chroots.opensuse_tumbleweed import TUMBLEWEED_ARCH, OpensuseTumbleweed
from coprtree.constants import (
    OPENSUSE_TUMBLEWEED_METALINK,
    OPENSUSE_TUMBLEWEED_PORTS_METALINK,
)
from coprtree.exceptions import UnsupportedDistribution

ALL_ARCHES = sorted(TUMBLEWEED_ARCH)
PORT_ARCHES = [arch for arch in ALL_ARCHES if arch != "x86_64"]


# ---------------------------------------------------------------------------
# __init__ / validation — rolling release, so `releases` is always empty
# and `release` stays None unless someone explicitly forces one
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("arch", ALL_ARCHES)
def test_init_accepts_every_known_arch(arch):
    """Every known arch constructs fine, with release left as None."""
    tumbleweed = OpensuseTumbleweed(release=None, arch=arch)
    assert tumbleweed.arch == arch
    assert tumbleweed.release is None


def test_init_rejects_unknown_arch():
    """Unknown arch raises."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        _ = OpensuseTumbleweed(release=None, arch="riscv64")


def test_init_rejects_empty_arch():
    """Empty arch raises too."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        _ = OpensuseTumbleweed(release=None, arch="")


def test_init_error_message_names_known_arches():
    """Bad-arch error names the bad value and every known arch."""
    with pytest.raises(UnsupportedDistribution) as exc_info:
        _ = OpensuseTumbleweed(release=None, arch="riscv64")
    message = str(exc_info.value)
    assert "riscv64" in message
    for arch in ALL_ARCHES:
        assert arch in message


def test_init_rejects_any_explicit_release():
    """Tumbleweed's `releases` is empty - any explicit release is rejected."""
    # unlike Fedora/Leap, there's no valid release to pass here at all;
    # only the default `release=None` is accepted
    with pytest.raises(UnsupportedDistribution, match="release"):
        _ = OpensuseTumbleweed(release="16.0", arch="x86_64")


def test_init_error_message_for_bad_release_names_the_distro():
    """The rejected-release error still names opensuse-tumbleweed."""
    with pytest.raises(UnsupportedDistribution) as exc_info:
        _ = OpensuseTumbleweed(release="16.0", arch="x86_64")
    assert "opensuse-tumbleweed" in str(exc_info.value)


# ---------------------------------------------------------------------------
# _match — pure shape recognition, no validation
# ---------------------------------------------------------------------------


def test_match_extracts_arch_with_no_release():
    """Splits a well-shaped chroot string into (None, arch)."""
    assert OpensuseTumbleweed._match("opensuse-tumbleweed-x86_64") == (None, "x86_64")


def test_match_extracts_even_an_unknown_arch():
    """_match only checks shape, not whether the arch value is actually valid."""
    assert OpensuseTumbleweed._match("opensuse-tumbleweed-riscv64") == (
        None,
        "riscv64",
    )


@pytest.mark.parametrize(
    "chroot",
    [
        "garbage",
        "",
        "opensuse",
        "opensuse-tumbleweed",
        "opensuse-tumbleweed-x86_64-extra",
        "-tumbleweed-x86_64",
        "debian-12-x86_64",
        "fedora-44-x86_64",
        "opensuse-leap-16.0-x86_64",
        "Opensuse-Tumbleweed-x86_64",  # case-sensitive
        "opensuse-Tumbleweed-x86_64",
    ],
)
def test_match_rejects_wrong_shape(chroot):
    """Anything not shaped like opensuse-tumbleweed-X comes back None."""
    assert OpensuseTumbleweed._match(chroot) is None


def test_match_accepts_empty_arch_segment_as_a_shape_match():
    """An empty arch segment still counts as a shape match."""
    # "opensuse-tumbleweed-" still has 3 parts and starts with
    # "opensuse-tumbleweed", so shape-wise it matches; the empty arch
    # itself is a semantic question for __init__/parse, not _match
    assert OpensuseTumbleweed._match("opensuse-tumbleweed-") == (None, "")


# ---------------------------------------------------------------------------
# parse — shape mismatch -> None, shape match but invalid value -> raises
# ---------------------------------------------------------------------------


def test_parse_returns_instance_for_valid_chroot():
    """A valid chroot string gives back a real OpensuseTumbleweed instance."""
    tumbleweed = OpensuseTumbleweed.parse("opensuse-tumbleweed-x86_64")
    assert isinstance(tumbleweed, OpensuseTumbleweed)
    assert tumbleweed.release is None
    assert tumbleweed.arch == "x86_64"


def test_parse_returns_none_for_malformed_shape():
    """A malformed shape gives back None, not an instance."""
    assert OpensuseTumbleweed.parse("garbage") is None
    assert OpensuseTumbleweed.parse("fedora-44-x86_64") is None
    assert OpensuseTumbleweed.parse("opensuse-tumbleweed") is None
    assert OpensuseTumbleweed.parse("opensuse-leap-16.0-x86_64") is None


def test_parse_raises_not_none_for_shape_match_but_bad_arch():
    """Shape matches but the arch is bad - raises, doesn't quietly return None."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        OpensuseTumbleweed.parse("opensuse-tumbleweed-riscv64")


# ---------------------------------------------------------------------------
# repos — the interesting part: x86_64 is the main tree, everything else
# is arch-split under /ports/<port_arch>/, and ppc64le's port dir isn't
# named after its own arch string
# ---------------------------------------------------------------------------


def test_repos_has_a_single_oss_repo():
    """Tumbleweed only ever has the one opensuse-tumbleweed repo."""
    repos = OpensuseTumbleweed(release=None, arch="x86_64").repos()
    ids = [repo_id for repo_id, _ in repos]
    assert ids == ["opensuse-tumbleweed"]


def test_repos_x86_64_uses_the_main_tree():
    """x86_64 is the only arch that lives on the main (non-ports) tree."""
    repos = dict(OpensuseTumbleweed(release=None, arch="x86_64").repos())
    assert repos["opensuse-tumbleweed"]["metalink"] == OPENSUSE_TUMBLEWEED_METALINK


@pytest.mark.parametrize("arch", PORT_ARCHES)
def test_repos_non_x86_64_uses_the_ports_tree(arch: str):
    """Every other arch lives under /ports/<port_arch>/tumbleweed/..."""
    repos = dict(OpensuseTumbleweed(release=None, arch=arch).repos())
    expected_port_arch = "ppc" if arch == "ppc64le" else arch
    assert repos["opensuse-tumbleweed"][
        "metalink"
    ] == OPENSUSE_TUMBLEWEED_PORTS_METALINK.format(port_arch=expected_port_arch)


def test_repos_ppc64le_is_remapped_to_ppc_in_the_ports_path():
    """openSUSE's ports tree names the ppc64le directory 'ppc', not 'ppc64le'."""
    repos = dict(OpensuseTumbleweed(release=None, arch="ppc64le").repos())
    metalink = repos["opensuse-tumbleweed"]["metalink"]
    assert "/ports/ppc/" in metalink
    assert "ppc64le" not in metalink


def test_init_accepts_i586():
    """i586 constructs fine - Tumbleweed really does build for it."""
    tumbleweed = OpensuseTumbleweed(release=None, arch="i586")
    assert tumbleweed.arch == "i586"
    assert tumbleweed.release is None


def test_match_extracts_i586():
    """_match recognizes an i586-shaped chroot string."""
    assert OpensuseTumbleweed._match("opensuse-tumbleweed-i586") == (None, "i586")


def test_parse_returns_instance_for_i586():
    """parse() gives back a real instance for the i586 chroot."""
    tumbleweed = OpensuseTumbleweed.parse("opensuse-tumbleweed-i586")
    assert isinstance(tumbleweed, OpensuseTumbleweed)
    assert tumbleweed.arch == "i586"


def test_repos_i586_uses_the_ports_tree():
    """i586 lives under /ports/, not the main x86_64 tree."""
    repos = dict(OpensuseTumbleweed(release=None, arch="i586").repos())
    assert repos["opensuse-tumbleweed"][
        "metalink"
    ] == OPENSUSE_TUMBLEWEED_PORTS_METALINK.format(port_arch="i586")


def test_repos_i586_is_not_remapped_like_ppc64le():
    """Unlike ppc64le -> ppc, i586's ports directory is named 'i586' itself."""
    repos = dict(OpensuseTumbleweed(release=None, arch="i586").repos())
    metalink = repos["opensuse-tumbleweed"]["metalink"]
    assert "/ports/i586/" in metalink


def test_str_format_for_i586():
    """str() gives back the canonical form for the i586 chroot."""
    assert str(OpensuseTumbleweed(release=None, arch="i586")) == (
        "opensuse-tumbleweed-i586"
    )


def test_get_chroot_dispatches_i586():
    """get_chroot routes the i586 chroot string to OpensuseTumbleweed."""
    chroot = get_chroot("opensuse-tumbleweed-i586")
    assert isinstance(chroot, OpensuseTumbleweed)
    assert chroot.arch == "i586"


def test_repos_are_recomputed_not_accumulated():
    """Calling repos() twice doesn't pile up duplicate entries."""
    tumbleweed = OpensuseTumbleweed(release=None, arch="x86_64")
    first = tumbleweed.repos()
    second = tumbleweed.repos()
    assert first == second
    assert first is not second


def test_str_format_has_no_release_segment():
    """str() omits the release segment entirely - tumbleweed has none."""
    tumbleweed = OpensuseTumbleweed(release=None, arch="x86_64")
    assert str(tumbleweed) == "opensuse-tumbleweed-x86_64"


@pytest.mark.parametrize("arch", ALL_ARCHES)
def test_str_round_trips_through_get_chroot(arch: str):
    """str() and get_chroot() are inverses of each other, for every arch."""
    original = OpensuseTumbleweed(release=None, arch=arch)
    reconstructed = get_chroot(str(original))
    assert reconstructed.release == original.release
    assert reconstructed.arch == original.arch


# ---------------------------------------------------------------------------
# get_chroot dispatch (package-level entrypoint most of the codebase uses)
# ---------------------------------------------------------------------------


def test_get_chroot_dispatches_to_opensuse_tumbleweed():
    """An opensuse-tumbleweed-shaped chroot string routes correctly."""
    assert isinstance(get_chroot("opensuse-tumbleweed-x86_64"), OpensuseTumbleweed)


def test_get_chroot_does_not_confuse_tumbleweed_with_leap():
    """The 3-part and 4-part opensuse chroots route to different classes."""
    assert isinstance(get_chroot("opensuse-tumbleweed-x86_64"), OpensuseTumbleweed)
    assert isinstance(get_chroot("opensuse-leap-16.0-x86_64"), OpensuseLeap)


def test_get_chroot_surfaces_tumbleweeds_own_validation_error():
    """Tumbleweed's own arch error isn't swallowed into the generic one."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        _ = get_chroot("opensuse-tumbleweed-riscv64")
