#!/usr/bin/env bash
# Do - The Simplest Build Tool on Earth.
# Documentation and examples see https://github.com/8gears/do

set -Eeuo pipefail # -e "Automatic exit from bash shell script on error"  -u "Treat unset variables and parameters as errors"

build() {
   echo "I am ${FUNCNAME[0]}ing"
   poetry build
}

test() {
   echo "I am ${FUNCNAME[0]}ing"
   flake8 pdme tests
   mypy pdme
   pytest
}

htmlcov() {
	pytest --cov-report=html
}

release() {
   ./scripts/release.sh
}

all() {
   build && test
}

"$@" # <- execute the task

[ "$#" -gt 0 ] || printf "Usage:\n\t./nixdo.sh %s\n" "($(compgen -A function | grep '^[^_]' | paste -sd '|' -))"
