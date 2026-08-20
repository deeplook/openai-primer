"""Generate a PNG image and write it to out/."""

import base64
from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    result = client.images.generate(
        model="gpt-image-1-mini",
        prompt="A tiny watercolor illustration of a friendly robot reading a book.",
        size="1024x1024",
    )
    image_data = result.data[0].b64_json
    if image_data is None:
        raise RuntimeError("The image response did not contain base64 image data")
    output = Path("out/robot.png")
    output.parent.mkdir(exist_ok=True)
    output.write_bytes(base64.b64decode(image_data))
    print(f"OK: wrote {output}")


if __name__ == "__main__":
    main()
