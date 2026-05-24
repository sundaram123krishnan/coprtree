from dataclasses import dataclass
from api import fetch_package_metadata
from dependency_graph import DependencyGraph, build_graph 


@dataclass(frozen=True)
class BuildTarget:
    provider: "pypi.org" # hardcode it for now, later we can support other providers
    name: str
    version: str | None = None


# only contains non-optional dependencies
@dataclass(frozen=True)
class DependencySpec:
    name: str
    requirement: str
    kind: str


@dataclass(frozen=True)
class PackageMetadata:
    provider: "pypi.org"
    name: str
    version: str
    dependencies: tuple[DependencySpec, ...]


class Coprtree:
    def __init__(self, target: BuildTarget):
        self.target = target
        self.metadata = fetch_package_metadata(target)
        # this would contain the full dependency graph, including nodes that fedora and copr repositories already provides
        self.graph = build_graph(self.metadata)

    def to_build(self) -> DependencyGraph:
        return to_build(self.graph)


if __name__ == "__main__":
    coprtree = Coprtree(BuildTarget(provider="pypi.org", name="django"))
    full_graph = coprtree.graph
    to_build = coprtree.to_build()
