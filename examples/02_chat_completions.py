"""Use the older, widely supported chat-completions interface."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Say hello in five words."}],
    )
    print("OK:", completion.choices[0].message.content)


if __name__ == "__main__":
    main()
