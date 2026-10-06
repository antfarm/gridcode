VENV := .venv/bin

.PHONY: install lint test docs serve-docs site clean

install:
	$(VENV)/pip install -e ".[docs,dev]"

lint:
	$(VENV)/ruff check src examples

test:
	$(VENV)/pytest

docs:
	$(VENV)/sphinx-build -E -a docs docs/_build

serve-docs:
	$(VENV)/sphinx-autobuild docs docs/_build

site: docs
	rm -rf site
	cp -R docs/_build site
	rm -rf site/_sources site/.buildinfo site/.doctrees

clean:
	rm -rf docs/_api docs/_build site
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
