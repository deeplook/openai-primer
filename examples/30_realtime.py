"""Send one text turn over a persistent Realtime API connection."""

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    with client.realtime.connect(model="gpt-realtime") as connection:
        connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Say hello in five words."}],
            }
        )
        connection.response.create()
        for event in connection:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
            if event.type == "response.done":
                print("\nOK: realtime response complete")
                return


if __name__ == "__main__":
    main()
