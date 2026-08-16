"""Generic singleton module"""

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Generic, TypeVar

from httpx import Client

from .constants import MAX_WORKERS, TIMEOUT

T = TypeVar("T")


class Singleton(Generic[T]):
    """Decorator that turns a function into a singleton"""

    def __init__(self, factory: Callable[[], T]) -> None:
        self._factory = factory
        self._instance: tuple[T] | None = None

    def __call__(self) -> T:
        if self._instance is None:
            self._instance = (self._factory(),)
        return self._instance[0]

    def cache_clear(self) -> None:
        """Reset the cached instance so the next call rebuilds it"""
        self._instance = None


@Singleton
def get_httpx_client() -> Client:
    """Returns singleton httpx client instance"""
    return Client(timeout=TIMEOUT)


@Singleton
def get_threadpool_executor() -> ThreadPoolExecutor:
    """Returns singleton thread pool executor instance"""
    return ThreadPoolExecutor(max_workers=MAX_WORKERS)
