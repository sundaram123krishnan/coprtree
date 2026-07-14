from __future__ import annotations

import sys
from typing import Any
from typing import IO


def write_line_b(
    s: bytes | None = None,
    stream: IO[bytes] = sys.stdout.buffer,
) -> None:
    if s is not None:
        stream.write(s)
    stream.write(b"\n")
    stream.flush()


def write_line(s: str | None = None, **kwargs: Any) -> None:
    write_line_b(s.encode() if s is not None else s, **kwargs)
