from __future__ import annotations

import logging
from collections.abc import Iterable

from coprtree.exceptions import CoprtreeError

from . import output
from .custom import CUSTOM_SOURCES

logger = logging.getLogger("coprtree")


def submit_levels(
    levels: Iterable[list],
    project: str,
    chroot: str,
) -> int:
    """Submit each build level to Copr as an ordered batch"""
    client, owner, name = _connect(project)

    prev_seed = None
    for index, level in enumerate(levels):
        output.write_line(f"level {index}:")
        seed = None
        for node in level:
            buildopts: dict = {"chroots": [chroot]}
            if seed is None and prev_seed is not None:
                buildopts["after_build_id"] = prev_seed
            elif seed is not None:
                buildopts["with_build_id"] = seed

            build = _submit_one(client, owner, name, node, chroot, buildopts)
            seed = seed or build.id
            output.write_line(f"  {node.name} {node.version} -> build {build.id}")
        prev_seed = seed
    return 0


def _connect(project: str):
    """Authenticate copr client"""
    try:
        from copr.v3 import Client
        from copr.v3 import CoprException
    except ImportError as e:
        raise CoprtreeError(
            "the 'copr' client is required to submit builds; install it "
            "(python3-copr, or `pip install copr`), or re-run with --dry-run"
        ) from e

    owner, name = project.split("/", 1)
    try:
        client = Client.create_from_config_file()
    except CoprException as e:
        raise CoprtreeError(f"could not initialize the Copr client: {e}") from e
    return client, owner, name


def _submit_one(client, owner, project, node, chroot, buildopts):
    """Submit one build to copr"""
    from copr.v3 import CoprException

    proxy = client.build_proxy
    try:
        match node.provider:
            case "pypi.org":
                return proxy.create_from_pypi(
                    ownername=owner,
                    projectname=project,
                    pypi_package_name=node.name,
                    pypi_package_version=node.version,
                    buildopts=buildopts,
                )
            case provider if provider in CUSTOM_SOURCES:
                custom = CUSTOM_SOURCES[provider]
                return proxy.create_from_custom(
                    ownername=owner,
                    projectname=project,
                    script=custom.script(node.name),
                    script_builddeps=list(custom.builddeps),
                    script_chroot=chroot,
                    script_resultdir=".",
                    buildopts=buildopts,
                )
            case _:
                raise CoprtreeError(
                    f"don't know how to submit provider {node.provider!r}"
                )
    except CoprException as e:
        raise CoprtreeError(f"build submission failed for {node.name}: {e}") from e
