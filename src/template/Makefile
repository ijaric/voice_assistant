include ../../common_makefile.mk

PROJECT_FOLDERS = bin lib tests


.PHONY: test
test:
	@echo 'Running tests...'
	@$(PYTHON) -m pytest tests/unit

.PHONY: ci-test
ci-test:
	@echo 'Running tests...'
	@$(PYTHON) -m pytest tests/unit
