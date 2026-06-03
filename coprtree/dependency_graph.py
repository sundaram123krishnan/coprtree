from dataclasses import dataclass

from .repo_check import has_package_in_repository
from .metadata import fetch_package_metadata
from .models import BuildTarget, Chroot, CoprProject, PackageMetadata


@dataclass(frozen=True)
class PackageNode:
    provider: str
    name: str
    version: str


class DependencyGraph:
    def __init__(self, target):
        self.target = target # root of the graph
        self._edges = {target: set()}


    def add_node(self, node: PackageNode):
        if node not in self._edges:
            self._edges[node] = set()


    def add_edge(self, from_node: PackageNode, to_node: PackageNode):
        self.add_node(to_node)
        self._edges[from_node].add(to_node)

    def walk(self, package: PackageMetadata, chroot: Chroot, project: CoprProject, visited=None) -> PackageNode:
        if visited is None:
            visited = {}
        if package.name in visited:
            return visited[package.name]

        node = PackageNode(package.provider, package.name, package.version)
        visited[package.name] = node
        self.add_node(node)
        for dependency in package.dependencies:
            if has_package_in_repository(dependency.name, chroot, project):
                continue
            child_package = fetch_package_metadata(BuildTarget(package.provider, dependency.name))
            child_node = self.walk(child_package, chroot, project, visited)
            self.add_edge(node, child_node)
        return node


def build_graph(root: PackageMetadata, chroot: Chroot, project: CoprProject) -> DependencyGraph:
    root_node = PackageNode(root.provider, root.name, root.version)
    graph = DependencyGraph(root_node)
    graph.walk(root, chroot, project)
    return graph


def build_levels(graph: DependencyGraph) -> list[list[PackageNode]]:
    remaining = {n: set(deps) for n, deps in graph._edges.items()}
    levels: list[list[PackageNode]] = []
    while remaining:
        ready = [n for n, deps in remaining.items() if not deps]
        if not ready:
            raise ValueError(f"Cycle in dependency graph among: {sorted(n.name for n in remaining)}")
        levels.append(sorted(ready, key=lambda n: n.name))
        for n in ready:
            del remaining[n]
        for deps in remaining.values():
            deps.difference_update(ready)
    return levels
