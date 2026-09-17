"""Opensuse leap chroot handler"""

from typing import ClassVar, override

from ..constants import OPENSUSE_LEAP_METALINK
from .base import Chroot, ReleaseArch, RepoSpec


class OpensuseLeap(Chroot):
    """A Opensuse leap chroot"""

    releases: ClassVar[tuple[str, ...]] = ("16.0",)

    def __init__(self, release: str, arch: str) -> None:
        super().__init__(arch=arch, release=release)

    @override
    def repos(self) -> list[RepoSpec]:
        repos: list[RepoSpec] = [
            (
                "opensuse-leap",
                {
                    "metalink": OPENSUSE_LEAP_METALINK.format(
                        release=self.release, arch=self.arch
                    )
                },
            )
        ]
        return repos

    @staticmethod
    @override
    def _match(chroot: str) -> ReleaseArch | None:
        parts = chroot.split("-")
        # prolly good for now, but need to better
        # think of how to improve it
        if len(parts) != 4 or parts[0] != "opensuse" or parts[1] != "leap":
            return None
        _, _, release, arch = parts
        return release, arch
