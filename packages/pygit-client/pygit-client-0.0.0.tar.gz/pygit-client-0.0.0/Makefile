ENV        = dev

VENV_DEV  := venv/dev
VBIN_DEV  := $(VENV_DEV)/bin

VENV_DOCS := venv/docs
VBIN_DOCS := $(VENV_DOCS)/bin

VENV      := $(VENV_$(shell echo '$(ENV)' | tr '[:lower:]' '[:upper:]'))
VBIN      := $(VENV)/bin

DOCS_SRC_DIR := docs
DOCS_BLD_DIR := docs/_build

setup: $(VBIN)/activate

interactive: $(VBIN)/activate
	$(VBIN)/python3

package: $(VBIN_DEV)/activate
	$(VBIN_DEV)/python3 -m build

upload-test: package
	$(VBIN_DEV)/python3 -m twine upload -r testpypi dist/* --non-interactive --verbose

upload: package
	$(VBIN_DEV)/python3 -m twine upload dist/* --non-interactive

test: $(VBIN_DEV)/activate
	$(VBIN_DEV)/pytest

html: $(VBIN_DOCS)/activate
	$(VBIN_DOCS)/sphinx-build -b html $(DOCS_SRC_DIR) $(DOCS_BLD_DIR)

$(VBIN_DEV)/activate: requirements-dev.txt requirements.txt
	python3 -m venv $(VENV_DEV)
	$(VBIN_DEV)/python3 -m pip install --upgrade pip
	$(VBIN_DEV)/pip install -r requirements-dev.txt

$(VBIN_DOCS)/activate: requirements-docs.txt
	python3 -m venv $(VENV_DOCS)
	$(VBIN_DOCS)/python3 -m pip install --upgrade pip
	$(VBIN_DOCS)/pip install -r requirements-docs.txt

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	rm -rf venv
	rm -rf dist
	rm -rf src/pygit_client.egg-info
	rm -rf .pytest_cache
	rm -rf docs/_build

 .PHONY: setup interactive package upload-test upload test clean
