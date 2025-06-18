install:
	uv sync --all-extras
	uv run pre-commit install

install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

install-python:
	uv python install

install-all: install-uv install-python install

lint:
	uv run pre-commit run --all-files

test-unit:
	rm -rf htmlcov
	uv run pytest -v \
		--cov-report term --cov-report html --cov=pyticktick \
		tests/unit

test-integration:
	rm -rf htmlcov
	uv run pytest -v \
		--cov-report term --cov-report html --cov=pyticktick \
		tests/integration

generate-v1-token: install
	uv run scripts/generate_v1_token.py

check-changelog: install
	uv run scripts/checks/changelog.py

build: install
	rm -rf dist/
	uv build

publish-dev:
	uv publish --index testpypi

publish:
	uv publish

publish-test:
	uv run --with pyticktick --no-project -- python -c "import pyticktick"

mkdocs-dev:
	uv run mkdocs serve

mkdocs-check:
	uv run mkdocs build --clean --strict

mkdocs-publish:
	uv run mkdocs gh-deploy --clean --force

generate-model-mermaid-diagrams:
	uv run pydantic-mermaid \
	    -m pyticktick/models/v1/__init__.py \
		-o docs/reference/models/v1/class_diagrams.md
	uv run pydantic-mermaid \
	    -m pyticktick/models/v2/__init__.py \
		-o docs/reference/models/v2/class_diagrams.md

	perl -i -0pe 's/classDiagram\n\n    class/classDiagram\n    direction LR\n    class/g' docs/reference/models/v1/class_diagrams.md
	perl -i -0pe 's/classDiagram\n\n    class/classDiagram\n    direction LR\n    class/g' docs/reference/models/v2/class_diagrams.md

	echo '\n!!! info\n    This was auto-generated code by [pydantic-2-mermaid](https://github.com/EricWebsmith/pydantic-2-mermaid).' >> docs/reference/models/v1/class_diagrams.md
	echo '\n!!! info\n    This was auto-generated code by [pydantic-2-mermaid](https://github.com/EricWebsmith/pydantic-2-mermaid).' >> docs/reference/models/v2/class_diagrams.md
