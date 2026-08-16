"""
httpx client singleton tests
"""

import httpx
import pytest

import coprtree.singleton as singleton_module
from coprtree.constants import TIMEOUT
from coprtree.singleton import get_httpx_client


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the module-level singleton before and after each test."""
    singleton_module._client = None  # pylint: disable=protected-access
    yield
    singleton_module._client = None  # pylint: disable=protected-access


def test_returns_an_httpx_client():
    """get_httpx_client returns an httpx.Client."""
    assert isinstance(get_httpx_client(), httpx.Client)


def test_repeated_calls_return_the_same_instance():
    """Repeated calls return the exact same object, not a new one."""
    first = get_httpx_client()
    second = get_httpx_client()
    assert first is second


def test_client_is_built_with_the_configured_timeout():
    """The built client uses TIMEOUT from constants.py."""
    client = get_httpx_client()
    assert client.timeout == httpx.Timeout(TIMEOUT)
