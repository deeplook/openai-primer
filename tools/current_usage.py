"""Print the current UTC day's completion-token totals for one project."""

import json
import os
from datetime import UTC, datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def main() -> None:
    admin_key = os.environ.get("OPENAI_ADMIN_KEY")
    project_id = os.environ.get("OPENAI_PROJECT_ID")
    if not admin_key or not project_id:
        print("SKIP: set OPENAI_ADMIN_KEY and OPENAI_PROJECT_ID")
        return

    start = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    query = urlencode(
        [
            ("start_time", int(start.timestamp())),
            ("bucket_width", "1d"),
            ("project_ids", project_id),
            ("group_by", "model"),
            ("limit", 1),
        ]
    )
    request = Request(
        f"https://api.openai.com/v1/organization/usage/completions?{query}",
        headers={"Authorization": f"Bearer {admin_key}"},
    )
    with urlopen(request, timeout=20) as response:
        payload = json.load(response)

    results = [result for bucket in payload["data"] for result in bucket["results"]]
    totals = {
        field: sum(result.get(field, 0) or 0 for result in results)
        for field in (
            "input_tokens",
            "input_cached_tokens",
            "output_tokens",
            "num_model_requests",
        )
    }
    print(
        "OK:",
        f"start_utc={start.isoformat()}",
        f"requests={totals['num_model_requests']}",
        f"input_tokens={totals['input_tokens']}",
        f"cached_input_tokens={totals['input_cached_tokens']}",
        f"output_tokens={totals['output_tokens']}",
    )
    for result in results:
        print(
            f"  {result.get('model')}: "
            f"input={result.get('input_tokens', 0)} "
            f"output={result.get('output_tokens', 0)}"
        )


if __name__ == "__main__":
    main()
