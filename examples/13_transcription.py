"""Transcribe an audio file named by AUDIO_FILE."""

import os
from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    audio_file = os.environ.get("AUDIO_FILE")
    if client is None:
        return
    if not audio_file:
        print("SKIP: set AUDIO_FILE=/path/to/audio.mp3 to transcribe audio")
        return

    path = Path(audio_file)
    with path.open("rb") as audio:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe", file=audio
        )
    print("OK:", transcription.text)


if __name__ == "__main__":
    main()
