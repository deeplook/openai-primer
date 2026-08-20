"""Use a chosen, trusted remote MCP server and explicitly approve its call."""

import os

from _shared import client_or_skip

MCP_MODEL = os.environ.get("OPENAI_MCP_MODEL", "gpt-5.6")
MCP_PROMPT = os.environ.get(
    "MCP_PROMPT",
    "List the available tools, then describe which one would answer a query.",
)


def describe_mcp_failure(status_code: int | None) -> str:
    if status_code == 424:
        return "MCP server tool discovery failed (HTTP 424); check the server URL and status"
    return "could not reach the MCP integration; check the server URL and network"


def main() -> None:
    client = client_or_skip()
    server_url = os.environ.get("MCP_SERVER_URL")
    if client is None:
        return
    if not server_url:
        print("SKIP: set MCP_SERVER_URL to a remote MCP server you trust")
        return

    tool = {
        "type": "mcp",
        "server_label": "trusted_mcp",
        "server_description": "A remote MCP server explicitly selected by this application.",
        "server_url": server_url,
        "require_approval": "always",
    }

    from openai import APIConnectionError, APIStatusError

    try:
        first = client.responses.create(
            model=MCP_MODEL,
            tools=[tool],
            input=MCP_PROMPT,
        )
    except APIStatusError as error:
        print(f"SKIP: {describe_mcp_failure(error.status_code)}")
        return
    except APIConnectionError:
        print(f"SKIP: {describe_mcp_failure(None)}")
        return
    approvals = [item for item in first.output if item.type == "mcp_approval_request"]
    if not approvals:
        print("OK:", first.output_text)
        return

    for approval in approvals:
        print(
            "Approval requested:",
            f"server={approval.server_label}",
            f"tool={approval.name}",
            f"arguments={approval.arguments}",
        )
    if os.environ.get("MCP_APPROVE") != "1":
        print("OK: review the request, then re-run with MCP_APPROVE=1 to approve it")
        return

    response = client.responses.create(
        model=MCP_MODEL,
        tools=[tool],
        previous_response_id=first.id,
        input=[
            {
                "type": "mcp_approval_response",
                "approval_request_id": approval.id,
                "approve": True,
            }
            for approval in approvals
        ],
    )
    print("OK:", response.output_text)


if __name__ == "__main__":
    main()
