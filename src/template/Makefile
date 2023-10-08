include ../../common_makefile.mk

PROJECT_FOLDERS = bin lib tests

ENV_FILE = .env

include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

.PHONY: test
test:
	@echo 'Running tests...'
	@$(PYTHON) -m pytest tests/unit
