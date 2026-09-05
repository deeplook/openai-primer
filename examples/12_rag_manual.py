"""Retrieve relevant passages by hand, then generate a grounded answer.

This is the simple-minded version of RAG (Retrieval-Augmented Generation):
embed a small in-memory corpus, rank it by cosine similarity to the query,
and stuff the top matches into the prompt. No vector database, no chunking
pipeline -- just a Python list. That is enough for a handful of documents;
past that, reach for a real vector store (see the module docstring at the
bottom for pointers).

`19_vector_store.py` / `20_file_search.py` show the managed equivalent,
where OpenAI does the chunking, embedding, and retrieval for you.
"""

import math

from _shared import MODEL, client_or_skip
from openai import OpenAI


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = 0.0
    left_norm = 0.0
    right_norm = 0.0
    for left_value, right_value in zip(left, right, strict=True):
        dot += left_value * right_value
        left_norm += left_value * left_value
        right_norm += right_value * right_value
    return dot / (math.sqrt(left_norm) * math.sqrt(right_norm))


CORPUS = [
    "The Eiffel Tower was completed in 1889 for the World's Fair in Paris.",
    "Mount Everest's summit sits 8,849 meters above sea level.",
    (
        "The Great Wall of China was built over several dynasties to guard "
        "the empire's northern borders."
    ),
    (
        "Photosynthesis converts sunlight, water, and carbon dioxide into "
        "glucose and oxygen."
    ),
]


def retrieve(
    client: OpenAI, query: str, corpus: list[str], top_k: int = 2
) -> list[str]:
    """Embed the query and corpus, then return the top_k closest passages."""
    embedded = client.embeddings.create(model="text-embedding-3-small", input=corpus)
    query_embedding = (
        client.embeddings.create(model="text-embedding-3-small", input=query)
        .data[0]
        .embedding
    )
    scored = [
        (cosine_similarity(query_embedding, item.embedding), text)
        for item, text in zip(embedded.data, corpus, strict=True)
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [text for _score, text in scored[:top_k]]


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    query = "How tall is the world's highest mountain?"
    passages = retrieve(client, query, CORPUS)

    prompt = (
        "Answer the question using only the context below.\n\n"
        "Context:\n- " + "\n- ".join(passages) + f"\n\nQuestion: {query}"
    )
    response = client.responses.create(model=MODEL, input=prompt)
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()


# This lesson re-embeds the whole corpus on every call to keep the example
# self-contained; a real system embeds documents once, persists the vectors,
# and only embeds the query at request time. For a real corpus (thousands of
# documents and up), an in-memory list also stops scaling: no persistence,
# no filtering, no chunking strategy, and an O(n) similarity scan per query.
# Options for the ambitious practitioner:
#
# - Qdrant (https://qdrant.tech) -- open-source vector database, easy to run
#   locally via Docker; see ~/dev/basic-rag-demo for a worked example that
#   pairs it with local embeddings.
# - pgvector (https://github.com/pgvector/pgvector) -- adds vector similarity
#   search to Postgres, useful if you already run Postgres.
# - sqlite-vec (https://github.com/asg017/sqlite-vec) -- an embeddable
#   vector index for SQLite, good for single-file/local-first apps.
# - OpenAI Vector Stores (19_vector_store.py / 20_file_search.py in this
#   primer) -- fully managed chunking, embedding, and retrieval.
