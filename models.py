from dataclasses import dataclass


@dataclass(frozen=True)
class BuildTarget:
    provider: "pypi.org"  # hardcode it for now, later we can support other providers
    name: str
    version: str | None = None


# only contains non-optional dependencies
@dataclass(frozen=True)
class DependencySpec:
    name: str
    requirement: str


@dataclass(frozen=True)
class PackageMetadata:
    provider: "pypi.org"
    name: str
    version: str
    dependencies: tuple[DependencySpec, ...]
