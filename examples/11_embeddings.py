"""Compare semantic similarity using normalized embedding vectors."""

import math

from _shared import client_or_skip


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Cosine similarity for OpenAI embeddings: just the dot product.

    text-embedding-3-* vectors are L2-normalized to length 1, so both
    norms in the cosine formula are 1. math.sumprod raises ValueError
    if the lengths differ.
    """
    return math.sumprod(left, right)


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    texts = ["A kitten sleeps on a sofa.", "A cat is resting indoors."]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    similarity = cosine_similarity(
        response.data[0].embedding, response.data[1].embedding
    )
    print(f"OK: cosine_similarity={similarity:.3f}")


if __name__ == "__main__":
    main()
