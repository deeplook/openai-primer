"""Upload training JSONL and create a fine-tuning job for a supported model."""

import os
from pathlib import Path

from _shared import client_or_skip

FINE_TUNING_MODEL = os.environ.get("FINE_TUNING_MODEL", "gpt-4.1-mini-2025-04-14")


def main() -> None:
    client = client_or_skip()
    path = Path("out/training.jsonl")
    if client is None:
        return
    if not path.exists():
        print("SKIP: run examples/25_fine_tuning_data.py first")
        return

    with path.open("rb") as handle:
        uploaded = client.files.create(file=handle, purpose="fine-tune")
    job = client.fine_tuning.jobs.create(
        training_file=uploaded.id, model=FINE_TUNING_MODEL
    )
    print(f"OK: job_id={job.id} status={job.status}")


if __name__ == "__main__":
    main()
