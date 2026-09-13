"""Shared Chroot interface every distro implementation builds on."""

from abc import ABC, abstractmethod
from typing import ClassVar, override

from ..exceptions import UnsupportedDistribution

RepoSpec = tuple[str, dict[str, str]]


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
    release: str
    arch: str

    def _check_valid_release(self, release: str) -> str:
        """Check if it's a valid release for that distribution"""
        name = type(self).__name__.lower()
        if release not in self.releases:
            raise UnsupportedDistribution(
                f"unsupported {name} release {release!r}; known: {self.releases}"
            )
        return release

    def __init__(self, arch: str, release: str | None = None) -> None:
        self.arch = _check_cpu_arch(arch)
        if release is not None:
            self.release = self._check_valid_release(release)

    @override
    def __str__(self) -> str:
        return type(self).__name__.lower() + "-" + self.release + "-" + self.arch

    @abstractmethod
    def repos(self) -> list[RepoSpec]:
        """Repo's to load for the particular chroot"""

    @classmethod
    @abstractmethod
    def parse(cls, chroot: str) -> Chroot | None:
        """Parse the given chroot and then return it's appropriate instance"""
