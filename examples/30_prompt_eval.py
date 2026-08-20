"""Run a tiny prompt regression set and report simple pass/fail results."""

from _shared import MODEL, client_or_skip

CASES = [("Reply only: A", "A"), ("Reply only: B", "B")]


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    passed = 0
    for prompt, expected in CASES:
        output = client.responses.create(model=MODEL, input=prompt).output_text.strip()
        passed += output == expected
        print(f"case={expected} actual={output!r}")
    print(f"OK: passed={passed}/{len(CASES)}")


if __name__ == "__main__":
    main()
