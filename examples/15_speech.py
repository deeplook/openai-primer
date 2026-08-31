"""Generate a short MP3 speech file in out/."""

from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    output = Path("out/hello.mp3")
    output.parent.mkdir(exist_ok=True)
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input="Hello from the OpenAI API primer.",
    ) as response:
        response.stream_to_file(output)
    print(f"OK: wrote {output}")


if __name__ == "__main__":
    main()
