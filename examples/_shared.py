"""Small helpers shared by the live API lessons."""

import os

MODEL = os.environ.get("OPENAI_MODEL", "gpt-5-mini")


def client_or_skip():
    """Return an SDK client, or print the local/offline path and stop."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("SKIP: set OPENAI_API_KEY to run this live API example")
        return None

    from openai import OpenAI

    return OpenAI()
