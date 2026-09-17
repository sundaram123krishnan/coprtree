"""
BuildEnv tests (hermetic: no dnf, no network)
"""

import pytest

from coprtree.chroots import Chroot
from coprtree.exceptions import InvalidCoprProject, UnsupportedDistribution
from coprtree.models import BuildEnv

# ---------------------------------------------------------------------------
# copr_project validation
# ---------------------------------------------------------------------------


def test_accepts_owner_project_form():
    """A normal owner/project string is stored as-is."""
    env = BuildEnv(["fedora-44-x86_64"], "owner/project")
    assert env.copr_project == "owner/project"


def test_rejects_project_without_slash():
    """No slash at all raises."""
    with pytest.raises(InvalidCoprProject, match="OWNER/PROJECT"):
        _ = BuildEnv(["fedora-44-x86_64"], "no-slash-here")


def test_rejects_empty_project():
    """Empty string raises too."""
    with pytest.raises(InvalidCoprProject):
        _ = BuildEnv(["fedora-44-x86_64"], "")


def test_error_message_names_the_bad_value():
    """The error actually names the value you passed in."""
    with pytest.raises(InvalidCoprProject, match="no-slash-here"):
        _ = BuildEnv(["fedora-44-x86_64"], "no-slash-here")


@pytest.mark.parametrize(
    "copr_project",
    [
        "/",  # bare slash: contains "/", so it's accepted as-is
        "/project",  # leading slash
        "owner/",  # trailing slash
        "owner/nested/project",  # more than two parts
    ],
)
def test_accepts_anything_containing_a_slash(copr_project: str):
    """The check is shape-only (contains "/"), not a strict two-part parse."""
    env = BuildEnv(["fedora-44-x86_64"], copr_project)
    assert env.copr_project == copr_project


def test_copr_project_is_validated_before_chroots():
    """Both bad at once - copr_project's error wins, it's checked first."""
    # both are invalid; copr_project is validated first (it's checked
    # before the chroots loop in __init__), so that's the error that
    # should surface
    with pytest.raises(InvalidCoprProject):
        _ = BuildEnv(["garbage"], "no-slash-here")


# ---------------------------------------------------------------------------
# chroots
# ---------------------------------------------------------------------------


def test_builds_chroot_objects_from_strings():
    """Chroot strings turn into real Chroot instances, not left as strings."""
    env = BuildEnv(["fedora-44-x86_64"], "owner/project")
    assert len(env.chroots) == 1
    assert isinstance(env.chroots[0], Chroot)
    assert str(env.chroots[0]) == "fedora-44-x86_64"


def test_builds_multiple_chroots_in_order():
    """Multiple chroots keep the order they were given in."""
    chroots = ["fedora-44-x86_64", "fedora-rawhide-x86_64"]
    env = BuildEnv(chroots, "owner/project")
    assert [str(c) for c in env.chroots] == chroots


def test_propagates_bad_chroot_error():
    """A malformed chroot string isn't swallowed, it raises."""
    with pytest.raises(UnsupportedDistribution):
        _ = BuildEnv(["garbage"], "owner/project")


def test_propagates_semantically_invalid_chroot_error():
    """A shape-valid but semantically bad chroot raises too."""
    with pytest.raises(UnsupportedDistribution, match="release"):
        _ = BuildEnv(["fedora-99-x86_64"], "owner/project")
