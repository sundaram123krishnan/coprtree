from __future__ import annotations

import functools
from types import SimpleNamespace
import dnf
import httpx

from .models import Chroot, CoprProject


COPR_URL = "https://copr.fedorainfracloud.org/api_3/package/list"
METALINK_URL = "https://mirrors.fedoraproject.org/metalink"
FEDORA_METALINK = f"{METALINK_URL}?repo=fedora-{{release}}&arch={{arch}}"
UPDATES_METALINK = f"{METALINK_URL}?repo=updates-released-f{{release}}&arch={{arch}}"


def _dnf_base_config(release: str, arch: str) -> dnf.base.Base:
    base = dnf.Base()
    base.conf.substitutions["releasever"] = release
    base.conf.substitutions["basearch"] = arch
    base.repos.add_new_repo(
        "fedora",
        base.conf,
        metalink=FEDORA_METALINK.format(release=release, arch=arch),
    )
    base.repos.add_new_repo(
        "updates",
        base.conf,
        metalink=UPDATES_METALINK.format(release=release, arch=arch),
    )
    return base

@functools.cache
def _fedora_sack(chroot: Chroot) -> dnf.sack.Sack:
    release, arch = _release_arch(chroot)
    base = _dnf_base_config(release, arch)
    # ignore the local rpmdb, we only care about that particular chroot repodata
    base.fill_sack(load_system_repo=False)
    return base.sack


def has_package_in_repository(name: str, chroot: Chroot, project: CoprProject) -> bool:
    if _in_fedora(name, chroot):
        return True
    if  _in_copr(name, project):
        return True
    return False


def _in_fedora(name: str, chroot: Chroot) -> bool:
    query = _fedora_sack(chroot).query().available().filter(provides=f"python3dist({name})")
    return bool(query.run())


def _in_copr(name: str, project: CoprProject) -> bool:
    #NOTE: for now when building the package follow the convention: `python-packagename`
    return f"python-{name}" in _copr_packages(project)


@functools.cache
def _copr_packages(project: CoprProject) -> frozenset[str]:
    owner, projectname = project.split("/", 1)
    response = httpx.get(
        COPR_URL,
        timeout=120,
        params={
            "ownername": owner,
            "projectname": projectname,
            "with_latest_succeeded_build": "true",
        },
    )
    listing = response.json(object_hook=lambda d: SimpleNamespace(**d))
    return frozenset(p.name for p in listing.items if p.builds.latest_succeeded is not None)


def _release_arch(chroot: Chroot) -> tuple[str, str]:
    # fedora-44-x86_64 -> ("44", "x86_64"); rawhides not handled 
    _, release, arch = chroot.split("-", 2)
    return release, arch
