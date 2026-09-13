from collections.abc import Callable
from dataclasses import dataclass

from coprtree.chroots import Chroot, get_chroot
from coprtree.exceptions import InvalidCoprProject


@dataclass(frozen=True)
class BuildTarget:
    provider: str
    name: str
    version: str | None = None


# i don't like it defined here, but good for now
class BuildEnv:  # pylint: disable=too-few-public-methods
    chroots: list[Chroot]
    copr_project: str

    def _validate_copr_project(self, copr_project: str) -> str:
        if "/" not in copr_project:
            raise InvalidCoprProject(
                f"copr project {copr_project!r} must be in 'OWNER/PROJECT' form"
            )
        return copr_project

    def __init__(self, chroots_str: list[str], copr_project: str):
        self.chroots = []
        self.copr_project = self._validate_copr_project(copr_project)
        # build the object for the respective chroots list
        for chroot in chroots_str:
            chroot_obj = get_chroot(chroot)
            self.chroots.append(chroot_obj)


# only contains non-optional dependencies
@dataclass(frozen=True)
class DependencySpec:
    name: str
    requirement: str


@dataclass(frozen=True)
class PackageMetadata:
    provider: str
    name: str
    version: str
    dependencies: tuple[DependencySpec, ...]


@dataclass(frozen=True)
class Provider:
    registry: str
    dep_kinds: frozenset[str]
    normalize: Callable[[str], str]
    provide: Callable[[str], str]
    version_constraints: Callable[[str], list[tuple[str, str]] | None]
    resolve_version: Callable[[str, str, list[str]], str]
