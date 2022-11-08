from email.mime.image import MIMEImage

from mail_cleaner.mail import send_mail_plus

PNG_DATA = (
    "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//"
    "8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
)


def test_send_mail_plus(mailoutbox):
    datauri = f"data:image/png;base64,{PNG_DATA}"

    text_message = "My Message\n"
    html_message = f'<p>My Message <img src="{datauri}" alt="my-image"></p>'
    attachments = [("file.bin", b"content", "application/foo")]

    send_mail_plus(
        "My Subject",
        text_message,
        "foo@sender.com",
        ["foo@bar.baz"],
        html_message=html_message,
        attachments=attachments,
    )

    assert len(mailoutbox) == 1

    message = mailoutbox[0]
    assert message.subject == "My Subject"
    assert message.recipients() == ["foo@bar.baz"]
    assert message.from_email == "foo@sender.com"

    # text
    assert message.body == "My Message\n"
    assert "<p>" not in message.body

    # html alternative
    assert len(message.alternatives) == 1
    content, mime_type = message.alternatives[0]
    assert mime_type == "text/html"
    assert "<p>My Message" in content

    # inline replaced datauri as img tag
    assert '<img src="cid:my-image-0" alt="my-image"/>' in content

    # same inline replaced datauri as attachment
    assert len(message.attachments) == 2
    file = message.attachments[0]
    assert isinstance(file, MIMEImage)
    assert file["Content-Type"] == "image/png"
    assert file["Content-ID"] == "<my-image-0>"

    # regular attachment
    file = message.attachments[1]
    assert file[0] == "file.bin"
    assert file[1] == b"content"  # still bytes
    assert file[2] == "application/foo"
