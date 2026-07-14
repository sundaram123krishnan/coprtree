from .constants import FEDORA_METALINK, UPDATES_METALINK
from .exceptions import UnsupportedDistribution
from .models import ChrootParts, ChrootSpec, RepoSpec

CPU_ARCH = {"x86_64", "aarch64", "ppc64le", "s390x"}


def _fedora_repos(release: str, arch: str) -> list[RepoSpec]:
    repos = [
        ("fedora", {"metalink": FEDORA_METALINK.format(release=release, arch=arch)})
    ]
    if release != "rawhide":
        repos.append(
            (
                "updates",
                {"metalink": UPDATES_METALINK.format(release=release, arch=arch)},
            )
        )
    return repos


FEDORA = ChrootSpec(
    name="fedora",
    releases=("43", "44", "rawhide"),
    repos=_fedora_repos,
)

_CHROOTS = {c.name: c for c in (FEDORA,)}


def get_distribution(name: str) -> ChrootSpec:
    if name not in _CHROOTS:
        raise UnsupportedDistribution(
            f"unsupported distribution {name!r}; known: {sorted(_CHROOTS)}"
        )
    return _CHROOTS[name]


def parse_chroot(chroot: str) -> ChrootParts:
    """Split a chroot into distro, release, arch."""
    parts = chroot.rsplit("-", 2)
    if len(parts) != 3 or not all(parts):
        raise UnsupportedDistribution(f"malformed chroot {chroot!r}")
    distro, release, arch = parts
    return distro, release, arch


def is_supported_chroot(chroot: str) -> bool:
    """Checks whether the provided chroot is supported or not"""
    try:
        distro, release, arch = parse_chroot(chroot)
        distribution = get_distribution(distro)
    except UnsupportedDistribution:
        return False
    return arch in CPU_ARCH and release in distribution.releases
