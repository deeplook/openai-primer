"""Upload a document and make it searchable with a vector store."""

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

    with Path(document).open("rb") as handle:
        uploaded = client.files.create(file=handle, purpose="user_data")
    store = client.vector_stores.create(name="primer documents")
    attachment = client.vector_stores.files.create(
        vector_store_id=store.id, file_id=uploaded.id
    )
    print(f"OK: vector_store_id={store.id} file_status={attachment.status}")


if __name__ == "__main__":
    main()
