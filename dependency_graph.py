from dataclasses import dataclass
from main import PackageMetadata, Provider


@dataclass(frozen=True)
class PackageNode:
    provider: Provider
    name: str
    version: str


@dataclass(frozen=True)
class DependencyGraph:
    target: PackageNode
    nodes: tuple[PackageNode, ...]
    edges: dict[PackageNode, tuple[PackageNode, ...]]


def build_graph(root: PackageMetadata) -> DependencyGraph:
    pass


def resolve_graph(graph: DependencyGraph) -> DependencyGraph:
    pass
