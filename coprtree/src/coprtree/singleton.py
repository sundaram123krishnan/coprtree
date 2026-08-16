"""Generic singleton module"""

import httpx

from .constants import TIMEOUT

_CLIENT: httpx.Client | None = None


def get_httpx_client() -> httpx.Client:
    """Returns singleton httpx client instance"""
    global _CLIENT  # pylint: disable=global-statement
    if _CLIENT is None:
        _CLIENT = httpx.Client(timeout=TIMEOUT)
    return _CLIENT
