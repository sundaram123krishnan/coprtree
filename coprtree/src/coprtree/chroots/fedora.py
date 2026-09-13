"""Fedora chroot handler"""

from typing import ClassVar, override

from ..constants import FEDORA_METALINK, UPDATES_METALINK
from .base import Chroot, RepoSpec


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
    def _match(chroot: str) -> tuple[str, str] | None:
        parts = chroot.split("-")
        if len(parts) != 3 or parts[0] != "fedora":
            return None
        _, release, arch = parts
        return release, arch

    @classmethod
    @override
    def parse(cls, chroot: str) -> Fedora | None:
        parts = cls._match(chroot)
        if parts is None:
            return None
        release, arch = parts
        return cls(release, arch)
