"""Pass an image URL beside text input."""

from _shared import MODEL, client_or_skip

IMAGE_URL = "https://openai-documentation.vercel.app/images/cat_and_otter.png"


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Describe this image in one sentence.",
                    },
                    {"type": "input_image", "image_url": IMAGE_URL},
                ],
            }
        ],
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
