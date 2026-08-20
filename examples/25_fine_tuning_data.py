"""Prepare the JSONL chat-training format required for fine-tuning uploads."""

import json
from pathlib import Path


def main() -> None:
    examples = [
        {
            "messages": [
                {"role": "user", "content": "ping"},
                {"role": "assistant", "content": "pong"},
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "up"},
                {"role": "assistant", "content": "down"},
            ]
        },
    ]
    output = Path("out/training.jsonl")
    output.parent.mkdir(exist_ok=True)
    output.write_text("".join(json.dumps(item) + "\n" for item in examples))
    print(f"OK: wrote {len(examples)} training examples to {output}")


if __name__ == "__main__":
    main()
