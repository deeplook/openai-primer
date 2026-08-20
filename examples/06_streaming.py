"""Stream output text as server-sent events arrive."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    stream = client.responses.create(
        model=MODEL, input="Write one short sentence about rain.", stream=True
    )
    print("OK:", end=" ")
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
