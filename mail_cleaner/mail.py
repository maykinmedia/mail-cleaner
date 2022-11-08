"""
Utility layer on top of :mod:`django.core.mail`.
"""
import logging
from email.mime.image import MIMEImage
from io import StringIO
from typing import TYPE_CHECKING, Iterable, List, Optional, Sequence, Tuple
from urllib.request import urlopen

from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils.text import slugify

from lxml import etree

if TYPE_CHECKING:
    from django.core.mail.message import _AttachmentTuple

__all__ = ["send_mail_plus"]

logger = logging.getLogger(__name__)


def send_mail_plus(
    subject: str,
    message: str,
    from_email: Optional[str],
    recipient_list: Optional[Sequence[str]],
    fail_silently: bool = False,
    auth_user: Optional[str] = None,
    auth_password: Optional[str] = None,
    connection=None,
    html_message: Optional[str] = None,
    attachments: Optional[Iterable["_AttachmentTuple"]] = None,
) -> int:
    """
    Send outgoing email.

    modified copy of :func:`django.core.mail.send_mail()` with:

    - attachment support
    - extract datauri images from html and attach as inline-attachments

    """

    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(
        subject, message, from_email, recipient_list, connection=connection
    )
    if html_message:
        html_message, mime_images = replace_datauri_images(html_message)

        mail.attach_alternative(html_message, "text/html")
        mail.mixed_subtype = "related"

        if mime_images:
            for cid, mime_type, content in mime_images:
                # note we don't pass mime_type because MIMEImage will make it
                # image/image/png
                image = MIMEImage(content)
                image.add_header("Content-ID", f"<{cid}>")
                mail.attach(image)

    if attachments:
        for attachment in attachments:
            filename, content, *extra = attachment
            mime_type = extra[0] if extra else None
            mail.attach(filename, content, mime_type)

    return mail.send()


_supported_datauri_replace_types = {
    "image/png",
    "image/jpg",
    "image/svg+xml",
}


def replace_datauri_images(html: str) -> Tuple[str, List[Tuple[str, str, bytes]]]:
    try:
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)
    except etree.ParseError:
        logger.error("replace_datauri_images() found a parse error in html text")
        return html, []

    mime_images = []

    for i, elem in enumerate(tree.iterfind(".//img")):
        src = elem.get("src")
        alt = elem.get("alt") or "image"
        if not src or not src.startswith("data:"):
            continue
        with urlopen(src) as response:
            data = response.read()
            content_type = response.headers["Content-Type"]
            if content_type not in _supported_datauri_replace_types:
                continue
            cid = f"{slugify(alt)}-{i}"
            elem.set("src", f"cid:{cid}")
            mime_images.append((cid, content_type, data))

    html = etree.tostring(tree.getroot(), pretty_print=True, encoding="utf8")

    return html.decode("utf8"), mime_images
