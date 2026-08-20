"""Make the smallest useful request with the Responses API."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(model=MODEL, input="Say hello in five words.")
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
