"""Upload a document named by DOCUMENT_FILE for a later API workflow."""

import os
from pathlib import Path

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    document = os.environ.get("DOCUMENT_FILE")
    if client is None:
        return
    if not document:
        print("SKIP: set DOCUMENT_FILE=/path/to/document.txt")
        return

    path = Path(document)
    with path.open("rb") as handle:
        uploaded = client.files.create(file=handle, purpose="user_data")
    print(f"OK: file_id={uploaded.id} filename={uploaded.filename}")


if __name__ == "__main__":
    main()
