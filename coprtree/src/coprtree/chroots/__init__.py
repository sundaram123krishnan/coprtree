"""Chroot dispatch: turn a chroot string into the right distro's instance."""

from ..exceptions import UnsupportedDistribution
from .base import Chroot
from .fedora import Fedora
from .opensuse_leap import OpensuseLeap
from .opensuse_tumbleweed import OpensuseTumbleweed

DISTRIBUTIONS: tuple[type[Chroot], ...] = (Fedora, OpensuseLeap, OpensuseTumbleweed)

__all__ = ["Chroot"]


def get_chroot(chroot: str) -> Chroot:
    """Parse given chroot into it's respective class"""
    for distribution in DISTRIBUTIONS:
        parsed = distribution.parse(chroot)
        if parsed is not None:
            return parsed
    raise UnsupportedDistribution(f"unsupported chroot {chroot!r}")
