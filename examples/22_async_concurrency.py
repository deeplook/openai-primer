"""Use AsyncOpenAI when several independent requests can run together."""

import asyncio

from _shared import MODEL


async def main() -> None:
    from _shared import client_or_skip

    if client_or_skip() is None:
        return
    from openai import AsyncOpenAI

    client = AsyncOpenAI()
    prompts = ["Reply only: red", "Reply only: blue", "Reply only: green"]
    responses = await asyncio.gather(
        *(client.responses.create(model=MODEL, input=prompt) for prompt in prompts)
    )
    print("OK:", [response.output_text for response in responses])


if __name__ == "__main__":
    asyncio.run(main())
