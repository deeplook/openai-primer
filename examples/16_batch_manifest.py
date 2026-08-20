"""Create a JSONL file ready for an asynchronous Batch API submission."""

import json
from pathlib import Path

from _shared import MODEL


def main() -> None:
    requests = [
        {
            "custom_id": "greeting-1",
            "method": "POST",
            "url": "/v1/responses",
            "body": {"model": MODEL, "input": "Reply only: hello"},
        },
        {
            "custom_id": "greeting-2",
            "method": "POST",
            "url": "/v1/responses",
            "body": {"model": MODEL, "input": "Reply only: goodbye"},
        },
    ]
    output = Path("out/requests.jsonl")
    output.parent.mkdir(exist_ok=True)
    output.write_text("".join(json.dumps(item) + "\n" for item in requests))
    print(f"OK: wrote {len(requests)} requests to {output}")


if __name__ == "__main__":
    main()
