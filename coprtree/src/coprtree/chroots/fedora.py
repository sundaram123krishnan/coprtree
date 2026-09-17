"""Fedora chroot handler"""

from typing import ClassVar, override

from ..constants import FEDORA_METALINK, UPDATES_METALINK
from .base import Chroot, ReleaseArch, RepoSpec


class Fedora(Chroot):
    """A Fedora chroot"""

    releases: ClassVar[tuple[str, ...]] = ("43", "44", "45", "rawhide")

    def __init__(self, release: str, arch: str) -> None:
        super().__init__(arch=arch, release=release)

    @override
    def repos(self) -> list[RepoSpec]:
        repos: list[RepoSpec] = [
            (
                "fedora",
                {
                    "metalink": FEDORA_METALINK.format(
                        release=self.release, arch=self.arch
                    )
                },
            )
        ]
        if self.release != "rawhide":
            repos.append(
                (
                    "updates",
                    {
                        "metalink": UPDATES_METALINK.format(
                            release=self.release, arch=self.arch
                        )
                    },
                )
            )
        return repos

    @staticmethod
    @override
    def _match(chroot: str) -> ReleaseArch | None:
        parts = chroot.split("-")
        if len(parts) != 3 or parts[0] != "fedora":
            return None
        _, release, arch = parts
        return release, arch
