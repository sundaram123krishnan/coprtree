"""Opensuse tumbleweed chroot handler"""

from typing import ClassVar, override

from ..constants import (
    OPENSUSE_TUMBLEWEED_METALINK,
    OPENSUSE_TUMBLEWEED_PORTS_METALINK,
)
from ..exceptions import UnsupportedDistribution
from .base import CPU_ARCH, Chroot, ReleaseArch, RepoSpec

# tumbleweed maps to ppc
_PORTS_ARCH = {"ppc64le": "ppc", "i586": "i586"}

TUMBLEWEED_ARCH = sorted((CPU_ARCH - {"s390x"}) | {"i586"})


class OpensuseTumbleweed(Chroot):
    """A Opensuse tumbleweed chroot"""

    releases: ClassVar[tuple[str, ...]] = ()
    arch: str

    def __init__(self, release: str | None, arch: str) -> None:
        if arch not in TUMBLEWEED_ARCH:
            raise UnsupportedDistribution(
                f"unsupported arch {arch!r}; known: {TUMBLEWEED_ARCH}"
            )
        super().__init__(arch=arch if arch in CPU_ARCH else "x86_64", release=release)
        self.arch = arch

    @override
    def repos(self) -> list[RepoSpec]:
        if self.arch == "x86_64":
            metalink = OPENSUSE_TUMBLEWEED_METALINK
        else:
            metalink = OPENSUSE_TUMBLEWEED_PORTS_METALINK.format(
                port_arch=_PORTS_ARCH.get(self.arch, self.arch)
            )
        return [("opensuse-tumbleweed", {"metalink": metalink})]

    @staticmethod
    @override
    def _match(chroot: str) -> ReleaseArch | None:
        parts = chroot.split("-")
        if len(parts) != 3 or parts[0] != "opensuse" or parts[1] != "tumbleweed":
            return None
        _, _, arch = parts
        return None, arch
