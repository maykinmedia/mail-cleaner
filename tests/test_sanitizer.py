from django.core.exceptions import SuspiciousOperation

import pytest

from mail_cleaner.sanitizer import sanitize_content


def test_strip_non_allowed_urls():
    body = (
        "<p>test https://google.com https://www.google.com https://allowed.com test</p>"
    )

    sanitized = sanitize_content(body, allowlist=["allowed.com"])

    assert sanitized == "<p>test   https://allowed.com test</p>"


def test_oversize_content_raise_suspiciosu_operation():
    body = "<p>My Message</p>" + ("123" * 1024 * 1024)

    with pytest.raises(SuspiciousOperation):
        sanitize_content(body, [])
