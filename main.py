from coprtree.coprtree import Coprtree
from coprtree.models import BuildTarget, Chroot, CoprProject


if __name__ == "__main__":
    coprtree = Coprtree(
        BuildTarget(provider="pypi.org", name="pydantic-ai"),
        copr_project=CoprProject("sundaram123krishnan/test"),
        chroot=Chroot("fedora-44-x86_64"),
    )
    # This is the topo-sorted pruned graph, so the siblings nodes of each levels can be built in parallel
    for i, level in enumerate(coprtree.build_graph_levels()):
        print(f"level {i}: {[n.name for n in level]}")
