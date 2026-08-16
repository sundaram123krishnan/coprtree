from coprtree.coprtree import resolve_dependencies
from coprtree.models import BuildEnv, BuildTarget

if __name__ == "__main__":
    levels = resolve_dependencies(
        BuildTarget(provider="pypi.org", name="pydantic-ai"),
        BuildEnv(
            chroot=["fedora-44-x86_64", "fedora-43-x86_64", "fedora-rawhide-x86_64"],
            copr_project="sundaram123krishnan/coprtree-test",
        ),
    )
    # This is the topo-sorted pruned graph, so the sibling nodes of each
    # level can be built in parallel
    for i, level in enumerate(levels):
        print(f"level {i}: {[n.name for n in level]}")
