from collections.abc import Iterable, Iterator
from dataclasses import replace

import httpx

from .dependency_graph import PackageNode, build_graph, build_levels
from .metadata import fetch_package_metadata
from .models import BuildEnv, BuildTarget
from .providers import get_provider

TIMEOUT = 120


def resolve_dependencies(
    target: BuildTarget,
    env: BuildEnv,
    dep_kinds: Iterable[str] | None = None,
) -> Iterator[list[PackageNode]]:
    provider = get_provider(target.provider)
    if dep_kinds:
        provider = replace(provider, dep_kinds=frozenset(dep_kinds))

    with httpx.Client(timeout=TIMEOUT) as client:
        metadata = fetch_package_metadata(target, provider, client)
        graph = build_graph(metadata, provider, env, client)
    return build_levels(graph)
