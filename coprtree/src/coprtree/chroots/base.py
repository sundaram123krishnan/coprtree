"""Shared Chroot interface every distro implementation builds on."""

import re
from abc import ABC, abstractmethod
from typing import ClassVar, Self, override

from ..exceptions import UnsupportedDistribution

type RepoSpec = tuple[str, dict[str, str]]
# None for rolling-releases
type ReleaseArch = tuple[str | None, str]

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")


CPU_ARCH = {"x86_64", "aarch64", "ppc64le", "s390x"}


def _check_cpu_arch(arch: str) -> str:
    """
    Check if the cpu architecture is supported
    """
    if arch not in CPU_ARCH:
        raise UnsupportedDistribution(
            f"unsupported arch {arch!r}; known: {sorted(CPU_ARCH)}"
        )
    return arch


class Chroot(ABC):
    """One distro's chroot: knows its own shape, validation, and repos."""

    releases: ClassVar[tuple[str, ...]] = ()
    release: str | None
    arch: str
    chroot_name: str

    @classmethod
    def _canonicalize_name(cls) -> str:
        """
        Canonicalize the class names to relevant chroots str representation
        """
        return _CAMEL_BOUNDARY.sub("-", cls.__name__).lower()

    def _check_valid_release(self, release: str) -> str:
        """Check if it's a valid release for that distribution"""
        if release not in self.releases:
            raise UnsupportedDistribution(
                f"unsupported {self.chroot_name} release {release!r}; "
                + f"known: {self.releases}"
            )
        return release

    def __init__(self, arch: str, release: str | None = None) -> None:
        self.chroot_name = self._canonicalize_name()
        self.arch = _check_cpu_arch(arch)
        self.release = (
            self._check_valid_release(release) if release is not None else None
        )

    @override
    def __str__(self) -> str:
        if self.release is None:
            return f"{self.chroot_name}-{self.arch}"
        return f"{self.chroot_name}-{self.release}-{self.arch}"

    @abstractmethod
    def repos(self) -> list[RepoSpec]:
        """Repo's to load for the particular chroot"""

    @staticmethod
    @abstractmethod
    def _match(chroot: str) -> ReleaseArch | None:
        """Match chroot's shape"""

    @classmethod
    def parse(cls, chroot: str) -> Self | None:
        """Parse the given chroot and then return it's appropriate instance"""
        parts = cls._match(chroot)
        if parts is None:
            return None
        release, arch = parts
        return cls(release=release, arch=arch)
