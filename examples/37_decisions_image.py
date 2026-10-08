"""Estimate visible product damage from a local image."""

import base64
import os
from pathlib import Path

from _shared import client_or_skip

client = client_or_skip()
if client:
    image_path = Path(
        os.environ.get(
            "IMAGE_PATH", str(Path(__file__).parent / "assets/product_broken.jpg")
        )
    )
    image_base64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    decision = client.decisions.create(
        model="gpt-6-luna",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Inspect the product in this photo.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ],
            }
        ],
        questions=[
            {
                "type": "predicate",
                "name": "visible_damage",
                "instructions": "Does the product have visible damage?",
            }
        ],
    )
    answer = decision.answers[0]
    if answer.type == "refusal":
        print(f"Refused: {answer.name}")
    elif answer.type == "predicate":
        print(f"Visible damage probability: {answer.probability}")
    else:
        raise TypeError(f"Unexpected answer type: {answer.type}")
