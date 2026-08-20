"""Compare semantic similarity using normalized embedding vectors."""

import math

from _shared import client_or_skip


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    return dot / math.sqrt(sum(a * a for a in left) * sum(b * b for b in right))


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
