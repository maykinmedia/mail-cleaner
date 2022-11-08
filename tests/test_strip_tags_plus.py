from django.core.exceptions import SuspiciousOperation

import pytest

from mail_cleaner.text import strip_tags_plus


def test_strip_tags_no_keep_leading_whitespace():
    markup = """
    <p>Some paragraph</p>



       <p>another paragraph</p>"""

    output = strip_tags_plus(markup)

    expected = "Some paragraph\n\nanother paragraph\n"
    assert output == expected


def test_strip_tags_keep_leading_whitespace():
    markup = """
Some plain text

with some
nested <p>markup</p>"""

    output = strip_tags_plus(markup, keep_leading_whitespace=True)

    expected = """Some plain text

with some
nested markup
"""
    assert output == expected


def test_oversize_content_raise_suspiciosu_operation():
    body = "<p>My Message</p>" + ("123" * 1024 * 1024)

    with pytest.raises(SuspiciousOperation):
        strip_tags_plus(body)


def test_unwrapping_anchors():
    markup = """
    <p>A paragraph

    with



    some newlines.
    </p>

    <p>
    There are <a href="https://example.com"><span>also</span></a> some
    <a href="https://example.com">links</a> in here.
    </p>
    """

    output = strip_tags_plus(markup)

    expected = """A paragraph

with

some newlines.

There are also (https://example.com) some
links (https://example.com) in here.

"""
    assert output == expected


def test_keep_leading_whitespace():
    markup = """
Plain text with bullets:

  - bullet <strong>1</strong>
  - bullet 2
    """

    output = strip_tags_plus(markup, keep_leading_whitespace=True)

    expected = """Plain text with bullets:

  - bullet 1
  - bullet 2

"""
    assert output == expected
