from argparse import ArgumentParser

from coprtree.constants import REGISTRY_BY_ALIAS

from . import __version__


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="coprtree",
        description="Resolve a package's dependency tree into parallel Copr "
        "build levels and submit them.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--project",
        required=True,
        metavar="OWNER/PROJECT",
        help="target Copr project",
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=sorted(REGISTRY_BY_ALIAS),
        help="Supported package ecosystems",
    )
    parser.add_argument("--package", required=True, help="name of the package to build")
    parser.add_argument(
        "--chroot",
        required=True,
        metavar="CHROOT",
        help="Copr chroot to build for, e.g. fedora-43-x86_64",
    )
    parser.add_argument(
        "--package-version",
        default=None,
        metavar="VERSION",
        help="package version to build (default: latest)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="resolve and print the build levels without submitting",
    )
    return parser
