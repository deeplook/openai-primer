"""List model IDs visible to this project; availability is account-specific."""

from _shared import client_or_skip


def main() -> None:
    client = client_or_skip()
    if client is None:
        return

    models = client.models.list()
    names = sorted(model.id for model in models.data)
    print(f"OK: models={len(names)} first={names[:5]}")


if __name__ == "__main__":
    main()
