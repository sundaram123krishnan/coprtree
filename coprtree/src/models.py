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
    provide: Callable[[str], str]
    version_constraints: Callable[[str], list[tuple[str, str]] | None]
    resolve_version: Callable[[str, str, list[str]], str]


RepoSpec = tuple[str, dict]
ChrootParts = tuple[str, str, str]


@dataclass(frozen=True)
class ChrootSpec:
    name: str
    releases: tuple[str, ...]
    repos: Callable[[str, str], list[RepoSpec]]
