"""Inspect response metadata useful for logging and cost accounting."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(model=MODEL, input="Reply only: OK")
    usage = response.usage
    print(
        "OK:",
        f"id={response.id}",
        f"status={response.status}",
        f"input_tokens={usage.input_tokens if usage else 'unknown'}",
        f"output_tokens={usage.output_tokens if usage else 'unknown'}",
    )


if __name__ == "__main__":
    main()
