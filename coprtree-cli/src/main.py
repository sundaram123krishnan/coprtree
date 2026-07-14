from __future__ import annotations

from argparse import ArgumentParser, Namespace

from coprtree.models import BuildEnv
from coprtree.models import BuildTarget
from coprtree.constants import REGISTRY_BY_ALIAS

from . import output
from .error_handler import error_handler
from .submit import submit_levels
from .build_parser import build_parser
from .supported_chroots import supported_chroots


def print_levels(levels) -> int:
    """Prints packages at each level"""
    for index, level in enumerate(levels):
        output.write_line(f"level {index}:")
        for node in level:
            output.write_line(f"  {node.name} {node.version}")
    return 0


def run(args: Namespace) -> int:
    """Submit the build levels as copr batch build"""
    from coprtree.coprtree import resolve_dependencies

    target = BuildTarget(
        provider=REGISTRY_BY_ALIAS[args.provider],
        name=args.package,
        version=args.package_version,
    )
    env = BuildEnv(chroot=args.chroot, copr_project=args.project)
    levels = resolve_dependencies(target, env)

    if args.dry_run:
        return print_levels(levels)
    return submit_levels(levels, args.project, args.chroot)


def validate_args(parser: ArgumentParser, args: Namespace) -> None:
    """Validate arguments"""
    match args:
        case _ if "/" not in args.project:
            parser.error("--project must be in 'OWNER/PROJECT' form")
        case _ if args.chroot not in supported_chroots():
            parser.error(f"--chroot {args.chroot!r} is not a supported chroot")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    with error_handler():
        validate_args(parser, args)
        return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
