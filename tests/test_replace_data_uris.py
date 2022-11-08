import base64

from mail_cleaner.mail import replace_datauri_images

PNG_DATA = (
    "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//"
    "8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
)


def test_replacement_basic():
    datauri = f"data:image/png;base64,{PNG_DATA}"
    input_html = f'<body><img src="{datauri}" alt="my-image"></body>'

    html, images = replace_datauri_images(input_html)

    assert isinstance(html, str)
    assert "data:image/" not in html

    assert len(images) == 1

    img = images[0]
    assert img[0] == "my-image-0"
    assert img[1] == "image/png"
    assert isinstance(img[2], bytes)
    assert img[2] == base64.b64decode(PNG_DATA)

    assert f' src="cid:{img[0]}"' in html


def test_replacement_basic_no_alt():
    datauri = f"data:image/png;base64,{PNG_DATA}"
    input_html = f'<body><img src="{datauri}"></body>'

    html, images = replace_datauri_images(input_html)

    assert isinstance(html, str)
    assert "data:image/" not in html

    assert len(images) == 1

    img = images[0]
    assert img[0] == "image-0"
    assert img[1] == "image/png"
    assert isinstance(img[2], bytes)
    assert img[2] == base64.b64decode(PNG_DATA)

    assert f' src="cid:{img[0]}"' in html


def test__replacement_skips_unsuppored_mimetypes():
    datauri = f"data:text/plain;base64,{PNG_DATA}"
    input_html = f'<body><img src="{datauri}" alt="my-image"></body>'

    html, images = replace_datauri_images(input_html)

    assert isinstance(html, str)
    assert datauri in html

    assert len(images) == 0


def test_replacement_skips_regular_urls():
    uri = "http://example/image.jpg"
    input_html = f'<body><img src="{uri}" alt="my-image"></body>'

    html, images = replace_datauri_images(input_html)

    assert isinstance(html, str)
    assert uri in html

    assert len(images) == 0
