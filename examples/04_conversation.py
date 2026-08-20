"""Continue a Responses API conversation without resending its history."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    first = client.responses.create(model=MODEL, input="My favorite fruit is mango.")
    second = client.responses.create(
        model=MODEL,
        previous_response_id=first.id,
        input="What fruit did I say I like?",
    )
    print("OK:", second.output_text)


if __name__ == "__main__":
    main()
