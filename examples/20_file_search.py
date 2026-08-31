"""Ask the Responses API to search an existing vector store."""

import os

from _shared import MODEL, client_or_skip


def main() -> None:
    client = client_or_skip()
    store_id = os.environ.get("VECTOR_STORE_ID")
    if client is None:
        return
    if not store_id:
        print("SKIP: set VECTOR_STORE_ID from 18_vector_store.py")
        return

    response = client.responses.create(
        model=MODEL,
        input="Summarize the documents in one sentence.",
        tools=[{"type": "file_search", "vector_store_ids": [store_id]}],
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
