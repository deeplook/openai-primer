"""Rate a bug report against ordered severity levels."""

from _shared import client_or_skip

client = client_or_skip()
if client:
    decision = client.decisions.create(
        model="gpt-6-luna",
        input="Export fails in Safari but works in Chrome.",
        questions=[
            {
                "type": "score",
                "name": "severity",
                "instructions": "How severe is this issue?",
                "levels": [
                    {
                        "label": "Cosmetic",
                        "description": "Appearance only; no lost functionality.",
                    },
                    {
                        "label": "Workaround available",
                        "description": "A task fails, but another way works.",
                    },
                    {
                        "label": "Fully blocked",
                        "description": "A task fails with no workaround.",
                    },
                ],
            }
        ],
    )
    answer = decision.answers[0]
    if answer.type == "refusal":
        print(f"Refused: {answer.name}")
    elif answer.type == "score":
        print(f"Severity: {answer.score} (confidence: {answer.confidence})")
    else:
        raise TypeError(f"Unexpected answer type: {answer.type}")
