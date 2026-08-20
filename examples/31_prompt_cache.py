"""Mark a stable prompt prefix so repeated calls can benefit from caching."""

from _shared import MODEL, client_or_skip

REFERENCE = """You are a concise travel assistant.
Always return one practical sentence. Never invent opening hours."""


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(
        model=MODEL,
        instructions=REFERENCE,
        input="Suggest an outdoor activity in Berlin.",
        prompt_cache_key="openai-primer-travel-assistant-v1",
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
