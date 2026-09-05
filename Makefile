.DEFAULT_GOAL := help
EXAMPLE ?= examples/01_first_response.py

.PHONY: help install format lint typecheck test run live-core usage clean-remote check-all clean

LIVE_CORE := examples/01_first_response.py examples/02_chat_completions.py \
	examples/03_instructions.py examples/04_conversation.py \
	examples/05_response_metadata.py examples/06_streaming.py \
	examples/07_structured_output.py examples/08_function_calling.py \
	examples/09_web_search.py examples/10_vision.py examples/11_embeddings.py \
	examples/12_rag_manual.py examples/13_moderation.py \
	examples/21_background_response.py \
	examples/22_async_concurrency.py examples/23_list_models.py \
	examples/31_prompt_eval.py examples/32_prompt_cache.py \
	examples/33_error_handling.py

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*## "}; {printf "  %-14s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --all-groups

format: ## Format examples and tests
	uv run ruff format examples tests tools
	uv run ruff check --fix examples tests tools

lint: ## Check formatting and linting
	uv run ruff format --check examples tests tools
	uv run ruff check examples tests tools

typecheck: ## Run strict mypy checks
	uv run mypy examples tests

test: ## Run offline smoke tests
	uv run python -m pytest -v

run: ## Run one example (requires OPENAI_API_KEY for live calls)
	uv run python $(EXAMPLE)

live-core: ## Run the conservative live-service subset (uses API credits)
	@for example in $(LIVE_CORE); do \
		echo "==> $$example"; \
		uv run python "$$example" || exit $$?; \
	done

usage: ## Query this UTC day's token usage (needs OPENAI_ADMIN_KEY and project ID)
	uv run python tools/current_usage.py

clean-remote: ## Delete or cancel only explicitly named remote resources
	uv run python examples/35_cleanup_resources.py

check-all: lint typecheck test ## Run all quality checks

clean: ## Remove caches and generated outputs
	rm -rf .pytest_cache .ruff_cache out
	find . -type d -name __pycache__ -exec rm -rf {} +
