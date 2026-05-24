from api import fetch_package_metadata
from dependency_graph import DependencyGraph, build_graph, resolve_graph
from models import BuildTarget


class Coprtree:
    def __init__(self, target: BuildTarget):
        self.target = target
        self.metadata = fetch_package_metadata(target)
        # this would contain the full dependency graph, including nodes that fedora and copr repositories already provides
        self.graph = build_graph(self.metadata)

    def to_build(self) -> DependencyGraph:
        return resolve_graph(self.graph)


if __name__ == "__main__":
    coprtree = Coprtree(BuildTarget(provider="pypi.org", name="flask"))
    print(coprtree.graph._edges)