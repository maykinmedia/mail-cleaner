=========
Changelog
=========

2.0.0 (2025-08-21)
==================

* Dropped support for Python < 3.10.
* Dropped support for Django < 4.2.
* Confirmed support for Python 3.12 and 3.13.
* Confirmed support for Django 5.2.
* Fixed crash in ``strip_tags_plus`` when anchors contain other elements than ``span``,
  like ``strong``.

1.2.0 (2023-06-13)
==================

* [#2] Add support for ``CC``.

1.1.0 (2023-01-18)
==================

Adds optional ``headers`` parameter to ``send_mail_plus``. These headers will
end up in the header section of the body of the top message, not in any
multipart "children" of the message.

1.0.0 (2022-11-08)
==================

Initial release of stable API

Three utilties are public API:

* ``send_mail_plus`` to handle (inline) attachments
* ``sanitize_content`` to strip untrusted/disallowed links from mail content
* ``strip_tags_plus`` to convert HTML into a best-effort plain text variant
