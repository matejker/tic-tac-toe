TEST_PATH=./tests

.PHONY: requirements
requirements:
	poetry install --no-dev

.PHONY: requirements_tools
requirements_tools:
	poetry install

.PHONY: lint
lint: requirements_tools
	poetry run flake8 --exclude=env,venv
	poetry run black --check .

.PHONY: test
test: requirements_tools
	poetry run pytest -vv --color=yes $(TEST_ONLY)

.PHONY: format
format: requirements_tools
	poetry run black .

.PHONY: typecheck
typecheck: requirements_tools
	poetry run mypy tests tic_tac_toe

.PHONY: notebook
notebook:
	poetry run jupyter notebook
