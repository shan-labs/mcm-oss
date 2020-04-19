.PHONY: all run test clean

all: run

run:
	python mcm_oss

test:
	@pytest
	@mypy --strict --follow-imports=skip mcm_oss
	@flake8 mcm_oss

clean:
# @find . -name "*cache*" -print
	@find . -name "*cache*" -exec rm -rf {} \+
