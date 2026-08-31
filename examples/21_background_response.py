"""Start a long-running response and poll until it reaches a terminal state."""

import os
import time

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    max_wait = int(os.environ.get("MAX_WAIT_SECONDS", "60"))
    response = client.responses.create(
        model=MODEL,
        input="Explain why leaves change color in two sentences.",
        background=True,
    )
    deadline = time.monotonic() + max_wait
    while response.status in {"queued", "in_progress"} and time.monotonic() < deadline:
        time.sleep(1)
        response = client.responses.retrieve(response.id)
    if response.status in {"queued", "in_progress"}:
        print(f"OK: timed out after {max_wait}s; response_id={response.id}")
        return
    print(f"OK: status={response.status} text={response.output_text}")


if __name__ == "__main__":
    main()
