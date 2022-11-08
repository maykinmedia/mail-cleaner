from django.core.exceptions import SuspiciousOperation

from .constants import MESSAGE_SIZE_LIMIT


def check_message_size(msg: str) -> None:
    if len(msg) > MESSAGE_SIZE_LIMIT:
        raise SuspiciousOperation("email content-length exceeded safety limit")
