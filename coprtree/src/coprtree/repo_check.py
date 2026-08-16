import functools
import os
from collections.abc import Callable

import dnf
import hawkey

from .chroots import get_distribution, parse_chroot
from .constants import CACHEDIR, COPR_BASEURL
from .models import BuildEnv, Provider
from .singleton import get_threadpool_executor


def _repo_adder(base: dnf.Base) -> Callable[..., dnf.repo.Repo]:
    return functools.partial(base.repos.add_new_repo, conf=base.conf)


@functools.cache
def _sack(chroot_name: str, copr_project: str) -> dnf.sack.Sack:
    distro, release, arch = parse_chroot(chroot_name)
    chroot = get_distribution(distro)
    base = dnf.Base()
    base.conf.cachedir = os.path.expanduser(
        CACHEDIR.format(chroot=chroot_name, project=copr_project.replace("/", "_"))
    )
    base.conf.substitutions["releasever"] = release
    base.conf.substitutions["basearch"] = arch
    base.conf.substitutions["arch"] = arch
    add_repo = _repo_adder(base)
    for repo_id, kwargs in chroot.repos(release, arch):
        add_repo(repo_id, **kwargs)
    add_repo(
        "copr",
        baseurl=[COPR_BASEURL.format(project=copr_project, chroot=chroot_name)],
    )
    # ignore the local rpmdb, we only care about that particular chroot repodata
    base.fill_sack(load_system_repo=False)
    return base.sack


def _check_package_version(sack, query, capability, constraints):
    for op, version in constraints:
        reldep = f"{capability} {op} {version}"
        query = query.filter(provides=hawkey.Reldep(sack, reldep))
    return query


def has_package_in_repository(
    provider: Provider, name: str, requirement: str, env: BuildEnv
) -> bool:
    constraints = provider.version_constraints(requirement)
    if constraints is None:
        return False
    capability = provider.provide(name)

    executor = get_threadpool_executor()
    futures = [
        executor.submit(_sack, chroot, env.copr_project) for chroot in env.chroot
    ]

    # concurrently building sacks for the same chroot race's dnf lock
    # file
    sacks = [future.result() for future in futures]

    for sack in sacks:
        query = sack.query().available()
        if constraints:
            query = _check_package_version(sack, query, capability, constraints)
        else:
            query = query.filter(provides=capability)
        if not bool(query.run()):
            return False
    return True
