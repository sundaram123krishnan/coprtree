from coprtree.coprtree import resolve_dependencies
from coprtree.models import BuildEnv, BuildTarget


if __name__ == "__main__":
    levels = resolve_dependencies(
        BuildTarget(provider="pypi.org", name="pydantic-ai"),
        BuildEnv(chroot="fedora-44-x86_64", copr_project="sundaram123krishnan/test"),
    )
    # This is the topo-sorted pruned graph, so the siblings nodes of each levels can be built in parallel
    for i, level in enumerate(levels):
        print(f"level {i}: {[n.name for n in level]}")
