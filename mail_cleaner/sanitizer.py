import logging
import re
from functools import partial
from typing import List, Optional
from urllib.parse import urlsplit

from .constants import URL_REGEX
from .utils import check_message_size

__all__ = ["sanitize_content"]

logger = logging.getLogger(__name__)


def sanitize_content(content: str, allowlist: Optional[List[str]] = None) -> str:
    """
    Sanitize the content by stripping untrusted content.

    This function is meant to protect against untrusted user input in e-mail bodies. It
    performs the following sanitizations:

    * strip URLs that are not present in the explicit allow list
    """
    check_message_size(content)

    # strip out any hyperlinks that are not in the configured allowlist
    allowlist = allowlist or []
    replace_urls = partial(sanitize_urls, allowlist)
    stripped = re.sub(URL_REGEX, replace_urls, content)

    return stripped


def sanitize_urls(allowlist: List[str], match) -> str:
    split_result = urlsplit(match.group())
    if split_result.netloc in allowlist:
        return match.group()

    logger.debug("Sanitized URL from email: %s", match.group())
    return ""
