from __future__ import annotations

import functools
from collections.abc import Callable

import dnf

from .models import BuildEnv, Provider

METALINK_URL = "https://mirrors.fedoraproject.org/metalink"
FEDORA_METALINK = f"{METALINK_URL}?repo=fedora-{{release}}&arch={{arch}}"
UPDATES_METALINK = f"{METALINK_URL}?repo=updates-released-f{{release}}&arch={{arch}}"
COPR_BASEURL = "https://download.copr.fedorainfracloud.org/results/{project}/{chroot}/"


def _repo_adder(base: dnf.Base) -> Callable[..., dnf.repo.Repo]:
    return functools.partial(base.repos.add_new_repo, conf=base.conf)


@functools.cache
def _sack(env: BuildEnv) -> dnf.sack.Sack:
    release, arch = _release_arch(env.chroot)
    base = dnf.Base()
    base.conf.substitutions["releasever"] = release
    base.conf.substitutions["basearch"] = arch
    add_repo = _repo_adder(base)
    add_repo("fedora", metalink=FEDORA_METALINK.format(release=release, arch=arch))
    add_repo("updates", metalink=UPDATES_METALINK.format(release=release, arch=arch))
    add_repo(
        "copr",
        baseurl=[COPR_BASEURL.format(project=env.copr_project, chroot=env.chroot)],
    )
    # ignore the local rpmdb, we only care about that particular chroot repodata
    base.fill_sack(load_system_repo=False)
    return base.sack


def has_package_in_repository(provider: Provider, name: str, env: BuildEnv) -> bool:
    query = (
        _sack(env).query().available().filter(provides=provider.fedora_provide(name))
    )
    return bool(query.run())


def _release_arch(chroot: str) -> tuple[str, str]:
    # fedora-44-x86_64 -> ("44", "x86_64"); rawhides not handled
    _, release, arch = chroot.split("-", 2)
    return release, arch
