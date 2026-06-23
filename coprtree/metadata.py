from types import SimpleNamespace

import httpx

from .constants import LATEST_VERSION_URL, VERSION_URL
from .exceptions import MetadataNotFound
from .models import BuildTarget, DependencySpec, PackageMetadata, Provider


def fetch_package_metadata(
    target: BuildTarget, provider: Provider, client: httpx.Client
) -> PackageMetadata:
    """Fetch metadata from ecosyste.ms for a package."""
    url = (
        VERSION_URL.format(
            provider=target.provider, name=target.name, version=target.version
        )
        if target.version
        else LATEST_VERSION_URL.format(provider=target.provider, name=target.name)
    )
    response = client.get(url)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise MetadataNotFound(
                f"no ecosyste.ms package for {target.name!r}"
            ) from error
        raise
    pkg = response.json(object_hook=lambda d: SimpleNamespace(**d))
    return PackageMetadata(
        provider=target.provider,
        name=target.name,
        version=pkg.number,
        dependencies=tuple(
            DependencySpec(
                name=provider.normalize(d.package_name), requirement=d.requirements
            )
            for d in pkg.dependencies
            if not d.optional and d.kind in provider.dep_kinds
        ),
    )
