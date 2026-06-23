from __future__ import annotations

import functools
from collections.abc import Callable

import dnf
import hawkey

from .constants import COPR_BASEURL, FEDORA_METALINK, UPDATES_METALINK
from .models import BuildEnv, Provider


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


def _check_package_version(sack, query, capability, constraints):
    for op, version in constraints:
        reldep = "{capability} {op} {version}".format(
            capability=capability, op=op, version=version
        )
        query = query.filter(provides=hawkey.Reldep(sack, reldep))
    return query


def has_package_in_repository(
    provider: Provider, name: str, requirement: str, env: BuildEnv
) -> bool:
    constraints = provider.version_constraints(requirement)
    if constraints is None:
        return False

    sack = _sack(env)
    capability = provider.fedora_provide(name)
    query = sack.query().available()
    if constraints:
        query = _check_package_version(sack, query, capability, constraints)
    else:
        query = query.filter(provides=capability)
    return bool(query.run())


def _release_arch(chroot: str) -> tuple[str, str]:
    # fedora-44-x86_64 -> ("44", "x86_64"); rawhides not handled
    _, release, arch = chroot.split("-", 2)
    return release, arch
