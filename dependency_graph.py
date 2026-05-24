from dataclasses import dataclass

from api import fetch_package_metadata
from models import BuildTarget, PackageMetadata


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

    def walk(self, package: PackageMetadata, visited=None) -> PackageNode:
        if visited is None:
            visited = {}
        if package.name in visited:
            return visited[package.name]

        node = PackageNode(package.provider, package.name, package.version)
        visited[package.name] = node
        self.add_node(node)
        for dependency in package.dependencies:
            child_package = fetch_package_metadata(BuildTarget(package.provider, dependency.name))
            child_node = self.walk(child_package, visited)
            self.add_edge(node, child_node)
        return node


def build_graph(root: PackageMetadata) -> DependencyGraph:
    root_node = PackageNode(root.provider, root.name, root.version)
    graph = DependencyGraph(root_node)
    graph.walk(root)
    return graph


def resolve_graph(graph: DependencyGraph) -> DependencyGraph:
    pass 

