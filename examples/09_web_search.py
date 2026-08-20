"""Use OpenAI-hosted web search; inspect citations in the full response if needed."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search"}],
        input="What is today's date? Cite a source.",
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
