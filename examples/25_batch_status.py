"""Retrieve a batch job named by BATCH_ID."""

import os
from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    batch_id = os.environ.get("BATCH_ID")
    if client is None:
        return
    if not batch_id:
        print("SKIP: set BATCH_ID from 23_submit_batch.py")
        return

    batch = client.batches.retrieve(batch_id)
    if batch.output_file_id is None:
        print(f"OK: status={batch.status} output_file_id=None")
        return

    output = Path("out") / f"{batch.id}-results.jsonl"
    output.parent.mkdir(exist_ok=True)
    client.files.content(batch.output_file_id).write_to_file(output)
    print(f"OK: status={batch.status} wrote={output}")


if __name__ == "__main__":
    main()
