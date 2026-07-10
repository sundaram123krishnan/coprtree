from .exceptions import UnsupportedProvider
from .models import Provider
from .normalize import (
    cpan_constraints,
    cpan_name,
    cpan_provide,
    cpan_resolve_version,
    pypi_constraints,
    pypi_name,
    pypi_provide,
    pypi_resolve_version,
)


PYPI = Provider(
    registry="pypi.org",
    dep_kinds=frozenset({"runtime"}),
    normalize=pypi_name,
    provide=pypi_provide,
    version_constraints=pypi_constraints,
    resolve_version=pypi_resolve_version,
)


CPAN = Provider(
    registry="metacpan.org",
    dep_kinds=frozenset({"configure", "build", "test", "runtime"}),
    normalize=cpan_name,
    provide=cpan_provide,
    version_constraints=cpan_constraints,
    resolve_version=cpan_resolve_version,
)


_PROVIDERS = {p.registry: p for p in (PYPI, CPAN)}


def get_provider(registry: str) -> Provider:
    if registry not in _PROVIDERS:
        raise UnsupportedProvider(
            f"unsupported provider {registry!r}; known: {sorted(_PROVIDERS)}"
        )
    return _PROVIDERS[registry]
