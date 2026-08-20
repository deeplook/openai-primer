"""Ask for JSON that conforms to a small, explicit schema."""

import json

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    response = client.responses.create(
        model=MODEL,
        input="Extract the city and country from: I live in Kyoto, Japan.",
        text={
            "format": {
                "type": "json_schema",
                "name": "location",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "country": {"type": "string"},
                    },
                    "required": ["city", "country"],
                    "additionalProperties": False,
                },
            }
        },
    )
    print("OK:", json.loads(response.output_text))


if __name__ == "__main__":
    main()
