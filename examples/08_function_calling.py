"""Let a model request a local function, then return the result safely."""

import json

from _shared import MODEL, client_or_skip

WEATHER_TOOL = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}


def get_weather(city: str) -> dict[str, str]:
    """A deterministic stand-in for a real, permissioned weather service."""
    return {"city": city, "forecast": "sunny", "temperature": "21 C"}


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    first = client.responses.create(
        model=MODEL,
        input="What is the weather in Berlin? Use the provided tool.",
        tools=[WEATHER_TOOL],
    )
    calls = [item for item in first.output if item.type == "function_call"]
    if not calls:
        print("OK: model answered without requesting a tool:", first.output_text)
        return

    outputs = []
    for call in calls:
        arguments = json.loads(call.arguments)
        result = get_weather(**arguments)
        outputs.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            }
        )
    final = client.responses.create(
        model=MODEL, previous_response_id=first.id, input=outputs
    )
    print("OK:", final.output_text)


if __name__ == "__main__":
    main()
