from functools import partial
import re

from .exceptions import UnsupportedProvider
from .models import Provider


def _provide(wrapper: str, name: str) -> str:
    return f"{wrapper}({name})"


def _perl_provide(name: str) -> str:
    return "perl" if name == "perl" else _provide("perl", name.replace("-", "::"))


PYPI = Provider(
    registry="pypi.org",
    dep_kinds=frozenset({"runtime"}),
    # pep 503 normalized names
    normalize=lambda n: re.sub(r"[-_.]+", "-", n.split("[", 1)[0]).lower(),
    fedora_provide=partial(_provide, "python3dist"),
)


CPAN = Provider(
    registry="metacpan.org",
    dep_kinds=frozenset({"configure", "build", "test", "runtime"}),
    normalize=lambda n: n,
    fedora_provide=_perl_provide,
)


_PROVIDERS = {p.registry: p for p in (PYPI, CPAN)}


def get_provider(registry: str) -> Provider:
    if registry not in _PROVIDERS:
        raise UnsupportedProvider(
            f"unsupported provider {registry!r}; known: {sorted(_PROVIDERS)}"
        )
    return _PROVIDERS[registry]
