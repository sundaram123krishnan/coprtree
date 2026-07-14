from functools import cache

import httpx

from coprtree.constants import TIMEOUT
from coprtree.chroots import is_supported_chroot
from coprtree.exceptions import CoprtreeError

_COPR_CHROOTS_LIST_URL = "https://copr.fedorainfracloud.org/api_3/mock-chroots/list"


@cache
def supported_chroots() -> tuple[str, ...]:
    """Chroots coprtree can resolve, from Copr's live chroot list."""
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.get(_COPR_CHROOTS_LIST_URL)
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise CoprtreeError(f"could not fetch the Copr chroot list: {e}") from e

    return tuple(sorted(name for name in response.json() if is_supported_chroot(name)))
