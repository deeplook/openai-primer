"""Classify text before sending it into a user-facing workflow."""

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    result = client.moderations.create(
        model="omni-moderation-latest", input="I would like to bake bread."
    ).results[0]
    print("OK:", f"flagged={result.flagged}")


if __name__ == "__main__":
    main()
