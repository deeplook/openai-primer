# OpenAI API Primer

[![CI](https://github.com/deeplook/openai-primer/actions/workflows/check.yml/badge.svg)](https://github.com/deeplook/openai-primer/actions/workflows/check.yml)
[![PyPI](https://img.shields.io/pypi/v/openai-primer.svg)](https://pypi.org/project/openai-primer/)
[![Python](https://img.shields.io/pypi/pyversions/openai-primer.svg)](https://pypi.org/project/openai-primer/)
[![Downloads](https://img.shields.io/pypi/dm/openai-primer.svg)](https://pepy.tech/project/openai-primer)
[![License](https://img.shields.io/pypi/l/openai-primer.svg)](https://pypi.org/project/openai-primer/)
[![Docs](https://img.shields.io/badge/docs-deeplook.github.io%2Fopenai--primer-blue)](https://deeplook.github.io/openai-primer)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/deeplook)

Small executable Python lessons for the OpenAI API. New OpenAI applications
should start with the Responses API; the Chat Completions lesson is included
because that interface is common among OpenAI-compatible vendors.

## Setup

```bash
uv sync --all-groups
export OPENAI_API_KEY="..."
export OPENAI_MODEL="gpt-5-mini"  # optional
uv run python examples/01_first_response.py
```

Without `OPENAI_API_KEY`, every networked lesson prints `SKIP` and exits
successfully. This keeps the test suite offline and cost-free.

## Modules

| File | Topic |
|---|---|
| `01_first_response.py` | First Responses API call |
| `02_chat_completions.py` | Portable chat-completions shape |
| `03_instructions.py` | Developer instructions and message input |
| `04_conversation.py` | Continue a conversation with `previous_response_id` |
| `05_response_metadata.py` | IDs, status, and token usage |
| `06_streaming.py` | Stream text deltas |
| `07_structured_output.py` | JSON Schema structured output |
| `08_function_calling.py` | Define, run, and return a local function tool |
| `09_web_search.py` | OpenAI-hosted web search |
| `10_vision.py` | Image URL input |
| `11_embeddings.py` | Text embeddings and cosine similarity |
| `12_rag_manual.py` | Manual RAG: embed a corpus, retrieve top-k, generate a grounded answer |
| `13_moderation.py` | Classify unsafe content |
| `14_transcription.py` | Transcribe a local audio file |
| `15_speech.py` | Generate speech to an MP3 file |
| `16_image_generation.py` | Generate a PNG image |
| `17_batch_manifest.py` | Build a JSONL manifest for the Batch API |
| `18_upload_file.py` | Upload a local file for later API use |
| `19_vector_store.py` | Create a vector store and add a file |
| `20_file_search.py` | Retrieve from an existing vector store |
| `21_background_response.py` | Start and bounded-poll a long-running response |
| `22_async_concurrency.py` | Make independent requests concurrently |
| `23_list_models.py` | Inspect models available to the project |
| `24_submit_batch.py` | Upload and submit a batch manifest |
| `25_batch_status.py` | Retrieve batch status and download completed results |
| `26_fine_tuning_data.py` | Prepare chat fine-tuning JSONL data |
| `27_create_fine_tuning_job.py` | Start a job from an uploaded training file |
| `28_image_edit.py` | Edit a supplied image |
| `29_video_generation.py` | Start, retrieve, and download a video-generation job |
| `30_realtime.py` | Exchange a text turn over the Realtime API |
| `31_prompt_eval.py` | Run a small regression test set |
| `32_prompt_cache.py` | Reuse a stable prompt prefix with prompt caching |
| `33_error_handling.py` | Handle API errors, retries, and request IDs |
| `34_remote_mcp.py` | Inspect and explicitly approve a remote MCP tool call |
| `35_cleanup_resources.py` | Delete or cancel explicitly named remote resources |

Run `make check-all` for offline formatting, linting, strict typing, and smoke tests.

To exercise the low-cost live subset after setting `OPENAI_API_KEY`, run
`make live-core`. This target uses API credits; the media, file, Batch,
fine-tuning, video, and Realtime lessons stay opt-in.

The MCP lesson deliberately has no default third-party server. Supply a remote
server you have reviewed and trust: `MCP_SERVER_URL=https://... uv run python
examples/34_remote_mcp.py`. Set `MCP_APPROVE=1` only after reviewing the
requested tool and arguments. Use `MCP_PROMPT="..."` to request a specific
read-only action and exercise the approval path.

For a tested public read-only example, use OpenAI's documented DeepWiki MCP
server. The first command only displays the approval request:

```bash
MCP_SERVER_URL=https://mcp.deepwiki.com/mcp \
MCP_PROMPT='Use read_wiki_structure for the openai/openai-python repository.' \
uv run python examples/34_remote_mcp.py
```

After reviewing the requested tool and arguments, add `MCP_APPROVE=1` to send
the approval response. A remote MCP server can receive model context and act on
external services, so use only servers whose operator and data practices you
trust.

Some advanced lessons create persistent remote resources. `make clean-remote`
only acts when `CONFIRM_CLEANUP=1` and one or more resource-ID variables are
provided: `VECTOR_STORE_ID`, `FILE_ID`, `BATCH_ID`, or `FINE_TUNING_JOB_ID`.
It deletes files/vector stores and cancels active jobs; it never searches for
or bulk-deletes resources.

`21_background_response.py` waits at most 60 seconds by default; override it
with `MAX_WAIT_SECONDS`. Re-run `29_video_generation.py` with
`VIDEO_ID=<id>` to retrieve a job and download a completed video.

To report today's project token usage, set an admin key plus the project ID,
then run `make usage`:

```bash
export OPENAI_ADMIN_KEY="..."
export OPENAI_PROJECT_ID="proj_..."
make usage
```

## Further reading

- [OpenAI API documentation](https://platform.openai.com/docs)
- [Responses API](https://platform.openai.com/docs/guides/responses)
- [Text generation](https://platform.openai.com/docs/guides/text)
- [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)
