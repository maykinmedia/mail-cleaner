"""
Utilities to convert HTML email into plain-text bodies.

Taken from Open Forms (EUPL 1.2 licensed), which used the code from other
Maykin Media projects.
"""
import re
from html import unescape
from typing import List

from django.utils.html import strip_tags as django_strip_tags

from lxml.html import fromstring, tostring

from .utils import check_message_size

__all__ = ["strip_tags_plus"]

RE_NON_WHITESPACE = re.compile(r"\S")

NEWLINE_CHARS = (
    "\n",
    "\r",
    "\r\n",
    "\v",
    "\x0b",
    "\f",
    "\x0c",
    "\x1c",
    "\x1d",
    "\x1e",
    "\x85",
    "\u2028",
    "\u2029",
)


def strip_tags_plus(text: str, keep_leading_whitespace: bool = False) -> str:
    """
    Strip HTML tags from input text.

    This utility wraps around django's :func:`django.utils.html.strip_tags` and cleans
    up the output to make it suitable for plain text display.

    .. warning:: This renders unescaped user-data and should **never** be used for
       display as HTML content (XSS risk).

    This is originally copied and modified from Maykin Media's "Werkbezoek" project.
    """
    text = unwrap_anchors(text)
    # <br> is eaten completely by strip_tags, so replace them by newlines
    text = text.replace("<br>", "\n")
    text = django_strip_tags(text)
    lines = text.splitlines()
    transformed_lines = transform_lines(
        lines, keep_leading_whitespace=keep_leading_whitespace
    )
    deduplicated_newlines = deduplicate_newlines(transformed_lines)

    return "".join(deduplicated_newlines)


def transform_lines(
    lines: List[str], keep_leading_whitespace: bool = False
) -> List[str]:
    transformed_lines = []

    for line in lines:
        unescaped_line = unescape(line)

        if (
            keep_leading_whitespace
            and unescaped_line.startswith(" ")
            and (match := RE_NON_WHITESPACE.search(unescaped_line)) is not None
        ):
            start = match.start()
            leading_whitespace = unescaped_line[:start]
            transformed = f"{' '.join(unescaped_line[start:].split())}".rstrip()
            split_line = f"{leading_whitespace}{transformed}"
        else:
            split_line = f"{' '.join(unescaped_line.split())}".rstrip()

        transformed_lines.append(f"{split_line}\n")

    return transformed_lines


def deduplicate_newlines(lines: List[str]) -> List[str]:
    deduplicated_newlines = []

    for line in lines:
        if not deduplicated_newlines:
            deduplicated_newlines.append(line)
            continue

        is_newline = line in NEWLINE_CHARS

        if is_newline and deduplicated_newlines[-1] in NEWLINE_CHARS:
            continue

        deduplicated_newlines.append(line)

    return deduplicated_newlines


def unwrap_anchors(html_str: str) -> str:
    """
    ugly util to append the href inside the anchor text so we can use strip-tags

    .. note:: this potentially runs on untrusted HTML content, which is why we apply an
       upper limit to the message size.
    """
    check_message_size(html_str)

    root = fromstring(html_str)

    for link in root.iterfind(".//a"):
        url = link.attrib.get("href", None)
        if not url:
            continue

        span_child = link.find(".//span")
        if not link.text and span_child is not None:
            # Issue open-formulieren/open-forms#2154
            # Case in which the link has a special colour, so it's wrapped in a span.
            span_child.text += f" ({url})"
        else:
            link.text += f" ({url})"

    return tostring(root, encoding="utf8").decode("utf8")
