"""Upload the local batch manifest and submit it for asynchronous processing."""

from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    path = Path("out/requests.jsonl")
    if client is None:
        return
    if not path.exists():
        print("SKIP: run examples/16_batch_manifest.py first")
        return

    with path.open("rb") as handle:
        uploaded = client.files.create(file=handle, purpose="batch")
    batch = client.batches.create(
        input_file_id=uploaded.id, endpoint="/v1/responses", completion_window="24h"
    )
    print(f"OK: batch_id={batch.id} status={batch.status}")


if __name__ == "__main__":
    main()
