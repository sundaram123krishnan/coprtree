from __future__ import annotations

import functools
import shlex
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent / "scripts"


def _script(path: Path, name: str) -> str:
    """Load a Copr custom-source script, filling in the package name."""
    return path.read_text().replace("@PACKAGE@", shlex.quote(name))


@dataclass(frozen=True)
class CustomSource:
    script: Callable[[str], str]
    builddeps: tuple[str, ...]


CUSTOM_SOURCES = {
    "metacpan.org": CustomSource(
        script=functools.partial(_script, _SCRIPTS / "cpanspec.sh"),
        builddeps=("cpanspec", "perl"),
    ),
}
