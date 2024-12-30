run:
	uv run -m --python3.12 riko

format:
	uvx ruff format .

check:
	uvx ruff check .
