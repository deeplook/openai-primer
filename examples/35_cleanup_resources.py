"""Delete or cancel only remote resources named explicitly in the environment."""

import os

from _shared import client_or_skip

RESOURCE_IDS = {
    "VECTOR_STORE_ID": "delete vector store",
    "FILE_ID": "delete file",
    "BATCH_ID": "cancel batch",
    "FINE_TUNING_JOB_ID": "cancel fine-tuning job",
}


def main() -> None:
    client = client_or_skip()
    resources = {
        name: os.environ[name] for name in RESOURCE_IDS if os.environ.get(name)
    }
    if client is None:
        return
    if not resources:
        print("SKIP: set one or more resource-ID variables to clean up")
        return
    if os.environ.get("CONFIRM_CLEANUP") != "1":
        actions = ", ".join(
            f"{RESOURCE_IDS[name]}={identifier}"
            for name, identifier in resources.items()
        )
        print(f"SKIP: would {actions}; re-run with CONFIRM_CLEANUP=1")
        return

    if identifier := resources.get("VECTOR_STORE_ID"):
        client.vector_stores.delete(identifier)
        print(f"OK: deleted vector_store={identifier}")
    if identifier := resources.get("FILE_ID"):
        client.files.delete(identifier)
        print(f"OK: deleted file={identifier}")
    if identifier := resources.get("BATCH_ID"):
        client.batches.cancel(identifier)
        print(f"OK: cancelled batch={identifier}")
    if identifier := resources.get("FINE_TUNING_JOB_ID"):
        client.fine_tuning.jobs.cancel(identifier)
        print(f"OK: cancelled fine_tuning_job={identifier}")


if __name__ == "__main__":
    main()
