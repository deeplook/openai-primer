"""Pass an image URL beside text input."""

from _shared import MODEL, client_or_skip
from openai.types.responses import (
    EasyInputMessageParam,
    ResponseInputImageParam,
    ResponseInputItemParam,
    ResponseInputMessageContentListParam,
    ResponseInputTextParam,
)

IMAGE_URL = "https://openai-documentation.vercel.app/images/cat_and_otter.png"


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    content: ResponseInputMessageContentListParam = [
        ResponseInputTextParam(
            type="input_text", text="Describe this image in one sentence."
        ),
        ResponseInputImageParam(type="input_image", image_url=IMAGE_URL, detail="auto"),
    ]
    message: EasyInputMessageParam = {"role": "user", "content": content}
    input_items: list[ResponseInputItemParam] = [message]
    response = client.responses.create(
        model=MODEL,
        input=input_items,
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
