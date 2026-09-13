"""
CLI Tests
"""

import pytest

from coprtree_cli.build_parser import build_parser
from coprtree_cli.custom import CUSTOM_SOURCES
from coprtree.constants import REGISTRY_BY_ALIAS

cpan_custom_script = CUSTOM_SOURCES["metacpan.org"].script

REQUIRED = {
    "--project": "me/test",
    "--provider": "pypi",
    "--package": "pydantic-ai",
    "--chroot": "fedora-43-x86_64",
}


def _argv(**overrides) -> list[str]:
    opts = {**REQUIRED, **overrides}
    return [tok for pair in opts.items() for tok in pair]


def test_parses_required_args():
    args = build_parser().parse_args(_argv())
    assert args.project == "me/test"
    assert args.provider == "pypi"
    assert args.package == "pydantic-ai"
    assert args.chroot == "fedora-43-x86_64"
    assert args.package_version is None
    assert args.dry_run is False


def test_dry_run_and_package_version_flags():
    args = build_parser().parse_args(
        _argv() + ["--dry-run", "--package-version", "1.2"]
    )
    assert args.dry_run is True
    assert args.package_version == "1.2"


@pytest.mark.parametrize("missing", list(REQUIRED))
def test_required_options_exit_2(missing):
    argv = [tok for k, v in REQUIRED.items() if k != missing for tok in (k, v)]
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(argv)
    assert exc.value.code == 2


def test_unknown_provider_rejected_by_choices():
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(_argv(**{"--provider": "rubygems"}))
    assert exc.value.code == 2


def test_provider_alias_mapping():
    assert REGISTRY_BY_ALIAS["pypi"] == "pypi.org"
    assert REGISTRY_BY_ALIAS["cpan"] == "metacpan.org"


def test_cpan_script_runs_cpanspec():
    script = cpan_custom_script("Mojolicious")
    assert script.startswith("#!/usr/bin/env bash\nset -e\n")
    assert "cpanspec" in script
    assert "Mojolicious" in script
    assert "$COPR_RESULTDIR" in script


def test_cpan_script_quotes_name():
    script = cpan_custom_script("Foo; echo hello")
    assert "'Foo; echo hello'" in script


def test_cpan_custom_source_builddeps():
    assert CUSTOM_SOURCES["metacpan.org"].builddeps == ("cpanspec", "perl")
