"""Edit an image supplied through IMAGE_FILE and save the resulting PNG."""

import base64
import os
from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    image_file = os.environ.get("IMAGE_FILE")
    if client is None:
        return
    if not image_file:
        print("SKIP: set IMAGE_FILE=/path/to/input.png")
        return

    with Path(image_file).open("rb") as image:
        result = client.images.edit(
            model="gpt-image-1-mini", image=image, prompt="Add a small red balloon."
        )
    image_data = result.data[0].b64_json
    if image_data is None:
        raise RuntimeError("The image response did not contain base64 image data")
    output = Path("out/edited.png")
    output.parent.mkdir(exist_ok=True)
    output.write_bytes(base64.b64decode(image_data))
    print(f"OK: wrote {output}")


if __name__ == "__main__":
    main()
