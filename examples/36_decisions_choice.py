"""Route a complaint to one of a fixed set of departments."""

from _shared import client_or_skip

client = client_or_skip()
if client:
    decision = client.decisions.create(
        model="gpt-6-luna",
        input="I was charged twice for my order.",
        questions=[
            {
                "type": "choice",
                "name": "department",
                "instructions": "Which department should handle this complaint?",
                "choices": [
                    {"value": "billing"},
                    {"value": "technical"},
                    {"value": "shipping"},
                    {"value": "other"},
                ],
            }
        ],
    )
    answer = decision.answers[0]
    if answer.type == "refusal":
        print(f"Refused: {answer.name}")
    elif answer.type == "choice":
        print(f"Department: {answer.choice} (confidence: {answer.confidence})")
    else:
        raise TypeError(f"Unexpected answer type: {answer.type}")
