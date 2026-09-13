"""
Fedora chroot tests
"""

# pylint: disable=protected-access

import pytest

from coprtree.chroots import get_chroot
from coprtree.chroots.base import CPU_ARCH
from coprtree.chroots.fedora import Fedora
from coprtree.constants import FEDORA_METALINK, UPDATES_METALINK
from coprtree.exceptions import UnsupportedDistribution

NUMBERED_RELEASES = ("43", "44", "45")
ALL_RELEASES = (*NUMBERED_RELEASES, "rawhide")
ALL_ARCHES = sorted(CPU_ARCH)


# ---------------------------------------------------------------------------
# __init__ / validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("release", ALL_RELEASES)
def test_init_accepts_every_known_release(release):
    """Every known release constructs fine."""
    fedora = Fedora(release, "x86_64")
    assert fedora.release == release
    assert fedora.arch == "x86_64"


@pytest.mark.parametrize("arch", ALL_ARCHES)
def test_init_accepts_every_known_arch(arch):
    """Every known arch constructs fine."""
    fedora = Fedora("44", arch)
    assert fedora.arch == arch


def test_init_rejects_unknown_release():
    """Unknown release raises."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        Fedora("99", "x86_64")


def test_init_rejects_empty_release():
    """Empty release raises too."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        Fedora("", "x86_64")


def test_init_rejects_unknown_arch():
    """Unknown arch raises."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        Fedora("44", "riscv64")


def test_init_rejects_empty_arch():
    """Empty arch raises too."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        Fedora("44", "")


def test_init_checks_arch_before_release():
    """Both invalid at once - arch's error wins, since it's checked first."""
    # both are invalid; arch is validated first (Chroot.__init__ checks
    # arch, then release) so that's the error that should surface
    with pytest.raises(UnsupportedDistribution, match="arch"):
        Fedora("99", "riscv64")


def test_init_error_message_names_the_distro_and_known_releases():
    """Bad-release error names fedora, the bad value, and what's known."""
    with pytest.raises(UnsupportedDistribution) as exc_info:
        Fedora("99", "x86_64")
    message = str(exc_info.value)
    assert "fedora" in message
    assert "99" in message
    assert repr(ALL_RELEASES) in message or str(ALL_RELEASES) in message


def test_init_error_message_names_known_arches():
    """Bad-arch error names the bad value and every known arch."""
    with pytest.raises(UnsupportedDistribution) as exc_info:
        Fedora("44", "riscv64")
    message = str(exc_info.value)
    assert "riscv64" in message
    for arch in ALL_ARCHES:
        assert arch in message


# ---------------------------------------------------------------------------
# _match — pure shape recognition, no validation
# ---------------------------------------------------------------------------


def test_match_extracts_release_and_arch():
    """Splits a well-shaped chroot string into (release, arch)."""
    assert Fedora._match("fedora-44-x86_64") == ("44", "x86_64")


def test_match_extracts_even_an_unknown_release():
    """_match only checks shape, not whether the values are actually valid."""
    assert Fedora._match("fedora-99-x86_64") == ("99", "x86_64")
    assert Fedora._match("fedora-44-riscv64") == ("44", "riscv64")


@pytest.mark.parametrize(
    "chroot",
    [
        "garbage",
        "",
        "fedora",
        "fedora-44",
        "fedora-44-x86_64-extra",
        "-44-x86_64",
        "debian-12-x86_64",
        "opensuse-leap-16.0-x86_64",
        "Fedora-44-x86_64",  # case-sensitive
    ],
)
def test_match_rejects_wrong_shape(chroot):
    """Anything not shaped like fedora-X-Y comes back None."""
    assert Fedora._match(chroot) is None


def test_match_accepts_empty_release_segment_as_a_shape_match():
    """An empty release segment still counts as a shape match."""
    # "fedora--x86_64" still has 3 parts and starts with "fedora", so
    # shape-wise it matches; the empty release itself is a semantic
    # question for __init__/parse, not _match
    assert Fedora._match("fedora--x86_64") == ("", "x86_64")


# ---------------------------------------------------------------------------
# parse — shape mismatch -> None, shape match but invalid value -> raises
# ---------------------------------------------------------------------------


def test_parse_returns_instance_for_valid_chroot():
    """A valid chroot string gives back a real Fedora instance."""
    fedora = Fedora.parse("fedora-44-x86_64")
    assert isinstance(fedora, Fedora)
    assert fedora.release == "44"
    assert fedora.arch == "x86_64"


def test_parse_returns_none_for_malformed_shape():
    """A malformed shape gives back None, not an instance."""
    assert Fedora.parse("garbage") is None
    assert Fedora.parse("debian-12-x86_64") is None
    assert Fedora.parse("fedora-44") is None


def test_parse_raises_not_none_for_shape_match_but_bad_release():
    """Shape matches but the release is bad - raises, doesn't quietly return None."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        Fedora.parse("fedora-99-x86_64")


def test_parse_raises_not_none_for_shape_match_but_bad_arch():
    """Shape matches but the arch is bad - raises, doesn't quietly return None."""
    with pytest.raises(UnsupportedDistribution, match="arch"):
        Fedora.parse("fedora-44-riscv64")


def test_parse_raises_for_empty_release_segment():
    """The empty-release edge case ends up raising too, end to end."""
    # "fedora--x86_64": _match matches the shape, parse then constructs
    # Fedora("", "x86_64"), which rejects the empty release
    with pytest.raises(UnsupportedDistribution, match="release"):
        Fedora.parse("fedora--x86_64")


# ---------------------------------------------------------------------------
# repos
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("release", NUMBERED_RELEASES)
def test_repos_numbered_release_has_fedora_and_updates(release):
    """Numbered releases get both the fedora and updates repo."""
    repos = Fedora(release, "x86_64").repos()
    ids = [repo_id for repo_id, _ in repos]
    assert ids == ["fedora", "updates"]


def test_repos_rawhide_has_no_updates():
    """Rawhide only gets the fedora repo, no updates repo to speak of."""
    repos = Fedora("rawhide", "x86_64").repos()
    ids = [repo_id for repo_id, _ in repos]
    assert ids == ["fedora"]


def test_repos_metalink_urls_are_correctly_formatted():
    """Metalink URLs match the real templates, not a hardcoded string."""
    fedora = Fedora("44", "x86_64")
    repos = dict(fedora.repos())
    assert repos["fedora"]["metalink"] == FEDORA_METALINK.format(
        release="44", arch="x86_64"
    )
    assert repos["updates"]["metalink"] == UPDATES_METALINK.format(
        release="44", arch="x86_64"
    )


def test_repos_are_recomputed_not_accumulated():
    """Calling repos() twice doesn't pile up duplicate entries."""
    fedora = Fedora("44", "x86_64")
    first = fedora.repos()
    second = fedora.repos()
    assert first == second
    assert first is not second


# ---------------------------------------------------------------------------
# __str__ (inherited from Chroot, only exercisable via a concrete subclass)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("release", ALL_RELEASES)
def test_str_format(release):
    """str() gives back the canonical distro-release-arch form."""
    assert str(Fedora(release, "x86_64")) == f"fedora-{release}-x86_64"


@pytest.mark.parametrize("release", ALL_RELEASES)
def test_str_round_trips_through_get_chroot(release):
    """str() and get_chroot() are inverses of each other."""
    original = Fedora(release, "x86_64")
    reconstructed = get_chroot(str(original))
    assert reconstructed.release == original.release
    assert reconstructed.arch == original.arch


# ---------------------------------------------------------------------------
# get_chroot dispatch (package-level entrypoint most of the codebase uses)
# ---------------------------------------------------------------------------


def test_get_chroot_dispatches_to_fedora():
    """A fedora-shaped chroot string routes to a Fedora instance."""
    assert isinstance(get_chroot("fedora-44-x86_64"), Fedora)


def test_get_chroot_raises_for_no_matching_distro():
    """Nothing claims it - generic unsupported-chroot error."""
    with pytest.raises(UnsupportedDistribution, match="unsupported chroot"):
        get_chroot("garbage")


def test_get_chroot_surfaces_fedoras_own_validation_error():
    """Fedora's own release error isn't swallowed into the generic one."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        get_chroot("fedora-99-x86_64")
