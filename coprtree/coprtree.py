from .metadata import fetch_package_metadata
from .dependency_graph import PackageNode, build_graph, build_levels
from .models import BuildTarget, Chroot, CoprProject


class Coprtree:
    def __init__(self, target: BuildTarget, copr_project: CoprProject, chroot: Chroot):
        self.target = target
        self.metadata = fetch_package_metadata(target)
        self.copr_project = copr_project
        self.chroot = chroot # later have options to add multipe chroots, for now keep only one
        self.graph = build_graph(self.metadata, chroot, copr_project)

    def build_graph_levels(self) -> list[list[PackageNode]]:
        return build_levels(self.graph)
