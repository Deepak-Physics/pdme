
# execute default build
default: build

# builds the python module using poetry
build:
	echo "building..."
	poetry build

# print a message displaying whether nix is being used
checknix:
	#!/usr/bin/env bash
	set -euxo pipefail
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		echo "In an interactive nix env."
	else
		echo "Using poetry as runner, no nix detected."
	fi

# run all tests
test: fmt
	#!/usr/bin/env bash
	set -euxo pipefail
	
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		echo "testing, using nix..."
		flake8 pdme tests
		mypy pdme
		pytest
	else
		echo "testing..."
		poetry run flake8 pdme tests
		poetry run mypy pdme
		poetry run pytest
	fi

# update all test snapshots, use if snapshots are out of date
update-snapshots:
		#!/usr/bin/env bash
		set -euxo pipefail
		if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
				pytest --snapshot-update
		else
				poetry run pytest --snapshot-update
		fi

# format code
fmt:
	#!/usr/bin/env bash
	set -euxo pipefail
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
	      black .
	else
		poetry run black .
	fi
	find pdme -type f -name "*.py" -exec sed -i -e 's/    /\t/g' {} \;
	find tests -type f -name "*.py" -exec sed -i -e 's/    /\t/g' {} \;

# release the app, checking that our working tree is clean and ready for release
release:
	./scripts/release.sh

htmlcov:
	poetry run pytest --cov-report=html
