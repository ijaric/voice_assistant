IMAGE_REGISTRY=ghcr.io/yp-middle-python-24
IMAGE_REPOSITORY=python-service-example-backend

PENV = .venv
NENV = ../node_modules
PYTHON = $(PENV)/bin/python
PYRIGHT = $(NENV)/.bin/pyright
TOML_SORT = $(PENV)/bin/toml-sort

PROJECT_FOLDERS = bin lib tests

.PHONY: init
init:
	@echo 'Installing python dependencies...'
	@poetry install

.PHONY: lint
lint:
	@echo 'Running poetry checks...'
	@poetry check

	@echo 'Running black checks...'
	@$(PYTHON) -m black --check .

	@echo 'Running isort checks...'
	@$(PYTHON) -m isort --check .

	@echo 'Running toml-sort checks...'
	@$(TOML_SORT) --check poetry.toml pyproject.toml
	@echo ''

	@echo 'Running pylint checks...'
	@$(PYTHON) -m pylint .

	@echo 'Running pyright checks...'
	@$(PYRIGHT)

.PHONY: lint-fix
lint-fix:
	@echo 'Running poetry autofixes...'
	@poetry check
	@poetry lock --no-update

	@echo 'Running black autofixes...'
	@$(PYTHON) -m black --safe .

	@echo 'Running isort autofixes...'
	@$(PYTHON) -m isort --atomic .

	@echo 'Running toml-sort autofixes...'
	@$(TOML_SORT) --in-place poetry.toml pyproject.toml

	@echo 'Running sort-all autofixes...'
	@find $(PROJECT_FOLDERS) -name '*.py' -type f -exec $(PYTHON) -m sort_all '{}' \;

	@echo 'Running pyupgrade autofixes...'
	@find $(PROJECT_FOLDERS) -name '*.py' -type f -exec $(PYTHON) -m pyupgrade --py310-plus '{}' \;

	@echo 'Running pylint checks...'
	@$(PYTHON) -m pylint .

	@echo 'Running pyright checks...'
	@$(PYRIGHT)

.PHONY: test
test:
	@echo 'Running tests...'
	@#$(PYTHON) -m pytest tests

.PHONY: clean
clean:
	@echo 'Cleaning python dependencies...'
	@rm -rf $(PENV)

	@echo 'Cleaning pytest cache...'
	@rm -rf .pytest_cache

	@echo 'Cleaning coverage results...'
	@rm -rf .coverage
	@rm -rf htmlcov

# Local development

.PHONY: dev-server-start
dev-server-start:
	@$(PYTHON) -m bin.main

# Test coverage

.PHONY: test-coverage-run
test-coverage-run:
	@echo 'Running test coverage...'
	@$(PYTHON) -m coverage run -m pytest tests

.PHONY: test-coverage-report
test-coverage-report:
	@$(PYTHON) -m coverage report -m

.PHONY: test-coverage-html
test-coverage-html:
	@$(PYTHON) -m coverage html
	@$(PYTHON) -m webbrowser -t htmlcov/index.html

# CI-specific

.PHONY: ci-image-build
ci-image-build:
	@echo 'Building image...'
	@docker build --tag $(IMAGE_REGISTRY)/$(IMAGE_REPOSITORY):$(IMAGE_TAG) .

.PHONY: ci-image-push
ci-image-push:
	@echo 'Uploading image...'
	@docker push $(IMAGE_REGISTRY)/$(IMAGE_REPOSITORY):$(IMAGE_TAG)
