from types import SimpleNamespace

import httpx

from models import BuildTarget, DependencySpec, PackageMetadata

BASE_URL = "https://packages.ecosyste.ms/api/v1"
LATEST_VERSION_URL = f"{BASE_URL}/registries/{{provider}}/packages/{{name}}/latest_version"
VERSION_URL = f"{BASE_URL}/registries/{{provider}}/packages/{{name}}/versions/{{version}}"


def fetch_package_metadata(target: BuildTarget) -> PackageMetadata:
    """Fetch metadata from ecosyste.ms for a package."""
    url = (
        VERSION_URL.format(provider=target.provider, name=target.name, version=target.version)
        if target.version
        else LATEST_VERSION_URL.format(provider=target.provider, name=target.name)
    )
    pkg = httpx.get(url).json(object_hook=lambda d: SimpleNamespace(**d))
    return PackageMetadata(
        provider=target.provider,
        name=target.name,
        version=pkg.number,
        dependencies=tuple(
            # this named resolutions needs to be relooked
            DependencySpec(name=d.package_name.split("[", 1)[0].lower(), requirement=d.requirements)
            for d in pkg.dependencies
            if not d.optional and d.kind == "runtime"
       ),
    )
