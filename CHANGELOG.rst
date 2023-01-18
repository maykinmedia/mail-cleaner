=========
Changelog
=========

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
