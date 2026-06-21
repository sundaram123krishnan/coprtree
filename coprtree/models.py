from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class BuildTarget:
    provider: str
    name: str
    version: str | None = None


@dataclass(frozen=True)
class BuildEnv:
    chroot: str
    copr_project: str


# only contains non-optional dependencies
@dataclass(frozen=True)
class DependencySpec:
    name: str
    requirement: str


@dataclass(frozen=True)
class PackageMetadata:
    provider: str
    name: str
    version: str
    dependencies: tuple[DependencySpec, ...]


@dataclass(frozen=True)
class Provider:
    registry: str
    dep_kinds: frozenset[str]
    normalize: Callable[[str], str]
    fedora_provide: Callable[[str], str]
