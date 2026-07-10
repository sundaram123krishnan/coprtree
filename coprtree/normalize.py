from functools import partial
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import Version

from .exceptions import CoprtreeError


def pypi_name(name: str) -> str:
    # ignore[] optional deps
    return canonicalize_name(name.split("[", 1)[0])


def cpan_name(name: str) -> str:
    return name


def _provide(wrapper: str, name: str) -> str:
    return f"{wrapper}({name})"


pypi_provide = partial(_provide, "python3dist")


def cpan_provide(name: str) -> str:
    return "perl" if name == "perl" else _provide("perl", name.replace("-", "::"))


matches = ["=", ">=", "<=", ">", "<"]
# 1.8.* not handled
not_handling = ["*", "~", "!"]

DELIMETER = ","


def get_operator_version(
    part: str, default_op: str | None = None
) -> tuple[str, str] | None:
    part = part.replace(" ", "")
    i = 0
    operator = ""
    while i < len(part) and not part[i].isdigit():
        operator += part[i]
        i += 1
    version = part[i:]
    operator = operator or default_op  # a bare version uses the default (CPAN: ">=")
    operator = "=" if operator == "==" else operator
    if operator not in matches or any(c in version for c in not_handling):
        return None
    return (operator, version)


def _constraints(
    requirement: str, default_op: str | None = None
) -> list[tuple[str, str]] | None:
    constraints = []
    for part in requirement.split(DELIMETER):
        result = get_operator_version(part, default_op)
        if result is None:
            return None
        constraints.append(result)
    return constraints


def pypi_constraints(requirement: str) -> list[tuple[str, str]] | None:
    if not requirement or requirement.strip() == "*":  # any version
        return []
    return _constraints(requirement)


def cpan_constraints(requirement: str) -> list[tuple[str, str]] | None:
    requirement = (requirement or "0").strip()
    if requirement in ("0", ""):
        return []
    return _constraints(requirement, default_op=">=")


def cpan_resolve_version(*_) -> str:
    """Resolve to cpan package version"""
    raise NotImplementedError("CPAN version resolution is not implemented")


def pypi_resolve_version(requirement: str, package_versions: list[str]) -> str:
    """Resolve to pypi package version"""
    if not requirement or requirement.strip() == "*":
        spec = SpecifierSet("")
    else:
        try:
            spec = SpecifierSet(requirement)
        except InvalidSpecifier as e:
            raise CoprtreeError(f"invalid version requirement {requirement!r}") from e
    candidates = list(spec.filter(package_versions))
    if not candidates:
        raise CoprtreeError(f"no released version satisfies {requirement!r}")
    return max(candidates, key=Version)
