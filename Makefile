TEST_FILE?="1"
PYTHON       = python3

.PHONY: default help all run test test-pytest lint-mypy lint-flake8 script clean

default: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  all          same as run target"
	@echo "  run          run the project interactively via cli"
	@echo "  test         runs lint-mypy lint-flake8 test-pytest targets"
	@echo "  test-pytest  run test cases"
	@echo "  lint-mypy    run mypy static type checker"
	@echo "  lint-flake8  run flake8 linter to 'verify pep8, pyflakes and circular complexity'"
	@echo "  clean        to remove cache files"

all: run

run:
	$(PYTHON) -m mcm_oss

test: test-pytest lint-flake8

test-pytest:
	@pytest

lint-mypy:
	@mypy --strict --follow-imports=skip mcm_oss

lint-flake8:
	@flake8 mcm_oss

script:
	@cat script_tests/${TEST_FILE}.txt | python -m mcm_oss

clean:
# @find . -name "*cache*" -print
	@find . -name "*cache*" -exec rm -rf {} \+
