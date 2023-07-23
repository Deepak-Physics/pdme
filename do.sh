#!/usr/bin/env bash
# Do - The Simplest Build Tool on Earth.
# Documentation and examples see https://github.com/8gears/do

set -Eeuo pipefail # -e "Automatic exit from bash shell script on error"  -u "Treat unset variables and parameters as errors"

checknix() {
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		echo "In an interactive nix env."
	else
		echo "Using poetry as runner, no nix detected."
	fi
}

build() {
	echo "I am ${FUNCNAME[0]}ing"
	poetry build
}

fmt() {
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		black .
	else
		poetry run black .
	fi
	find . -type f -name "*.py" -exec sed -i -e 's/    /\t/g' {} \;
}

test() {
	echo "I am ${FUNCNAME[0]}ing"
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		flake8 pdme tests
		mypy pdme
		pytest
	else
		poetry run flake8 pdme tests
		poetry run mypy pdme
		poetry run pytest
	fi
}

updatesnap() {
	echo "I am ${FUNCNAME[0]}ing"
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		pytest --snapshot-update
	else
		poetry run pytest --snapshot-update
	fi
}

htmlcov() {
	if [[ "${DO_NIX_CUSTOM:=0}" -eq 1 ]]; then
		pytest --cov-report=html
	else
		poetry run pytest --cov-report=html
	fi
}

release() {
	./scripts/release.sh
}

all() {
	build && fmt && test
}

"$@" # <- execute the task

[ "$#" -gt 0 ] || printf "Usage:\n\t./do.sh %s\n" "($(compgen -A function | grep '^[^_]' | paste -sd '|' -))"
