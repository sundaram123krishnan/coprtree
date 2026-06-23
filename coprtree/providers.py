from .exceptions import UnsupportedProvider
from .models import Provider
from .normalize import (
    cpan_constraints,
    cpan_name,
    cpan_provide,
    pypi_constraints,
    pypi_name,
    pypi_provide,
)


PYPI = Provider(
    registry="pypi.org",
    dep_kinds=frozenset({"runtime"}),
    normalize=pypi_name,
    fedora_provide=pypi_provide,
    version_constraints=pypi_constraints,
)


CPAN = Provider(
    registry="metacpan.org",
    dep_kinds=frozenset({"configure", "build", "test", "runtime"}),
    normalize=cpan_name,
    fedora_provide=cpan_provide,
    version_constraints=cpan_constraints,
)


_PROVIDERS = {p.registry: p for p in (PYPI, CPAN)}


def get_provider(registry: str) -> Provider:
    if registry not in _PROVIDERS:
        raise UnsupportedProvider(
            f"unsupported provider {registry!r}; known: {sorted(_PROVIDERS)}"
        )
    return _PROVIDERS[registry]
