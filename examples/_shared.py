"""Small helpers shared by the live API lessons."""

import os

from openai import OpenAI

MODEL = os.environ.get("OPENAI_MODEL", "gpt-5-mini")


def client_or_skip() -> OpenAI | None:
    """Return an SDK client, or print the local/offline path and stop."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("SKIP: set OPENAI_API_KEY to run this live API example")
        return None

    return OpenAI()
