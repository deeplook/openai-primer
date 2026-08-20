"""Start a video job, or retrieve and download a video named by VIDEO_ID."""

import os
from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    video_id = os.environ.get("VIDEO_ID")
    if video_id:
        video = client.videos.retrieve(video_id)
        if video.status != "completed":
            print(f"OK: video_id={video.id} status={video.status}")
            return
        output = Path("out") / f"{video.id}.mp4"
        output.parent.mkdir(exist_ok=True)
        client.videos.download_content(video.id).write_to_file(output)
        print(f"OK: status=completed wrote={output}")
        return

    video = client.videos.create(
        model="sora-2", prompt="A paper airplane gliding across a sunny blue sky."
    )
    print(
        f"OK: video_id={video.id} status={video.status}; re-run with VIDEO_ID={video.id}"
    )


if __name__ == "__main__":
    main()
