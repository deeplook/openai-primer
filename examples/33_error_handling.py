"""Handle expected API failures without exposing a key or full request body."""

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    from openai import APIConnectionError, APIStatusError, RateLimitError

    try:
        response = client.responses.create(
            model=MODEL, input="Reply only: OK", timeout=20
        )
    except RateLimitError as error:
        print(f"OK: rate limited; retry later (request_id={error.request_id})")
    except APIConnectionError:
        print("OK: connection failed; retry with backoff")
    except APIStatusError as error:
        print(f"OK: API status={error.status_code} request_id={error.request_id}")
    else:
        print("OK:", response.output_text)


if __name__ == "__main__":
    main()
