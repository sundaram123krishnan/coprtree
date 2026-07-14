from __future__ import annotations

import contextlib
import sys
import traceback
from collections.abc import Generator

from coprtree.exceptions import CoprtreeError

from . import output


@contextlib.contextmanager
def error_handler() -> Generator[None]:
    """Turn exceptions into clean messages and exit codes."""
    try:
        yield
    except CoprtreeError as e:
        _fail(f"{type(e).__name__}: {e}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        _fail("interrupted (^C)")
        raise SystemExit(130)
    except Exception:
        _fail("an unexpected error occurred")
        output.write_line_b(traceback.format_exc().encode(), stream=sys.stderr.buffer)
        raise SystemExit(3)


def _fail(message: str) -> None:
    output.write_line(f"coprtree: {message}", stream=sys.stderr.buffer)
