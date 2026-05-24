from metadata import fetch_package_metadata
from dependency_graph import DependencyGraph, build_graph, resolve_graph
from models import BuildTarget


class Coprtree:
    def __init__(self, target: BuildTarget, copr_project: str | None, chroot: str | None):
        self.target = target
        self.metadata = fetch_package_metadata(target)
        # this would contain the full dependency graph, including nodes that fedora and copr repositories already provides
        self.graph = build_graph(self.metadata)
        self.copr_project = copr_project
        self.chroot = chroot # later have options to add multipe chroots, for now keep only one

    def to_build(self) -> DependencyGraph:
        return resolve_graph(self.graph, self.chroot, self.copr_project)


if __name__ == "__main__":
    coprtree = Coprtree(
        BuildTarget(provider="pypi.org", name="pydantic-ai"),
        copr_project=None,
        chroot="fedora-rawhide-x86_64",
    )
    print("full graph:", coprtree.graph._edges)
    print()
    print("to build:  ", coprtree.to_build()._edges)