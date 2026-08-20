"""Separate application instructions from a user's request."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(
        model=MODEL,
        instructions="Reply as a concise museum guide.",
        input="Describe a sundial.",
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
