#!/usr/bin/env bash

set -e


poetry export --without-hashes --dev -f requirements.txt -o requirements-dev.txt
poetry export -f requirements.txt -o requirements.txt

# remove the -e parameter added by poetry when installind a dependency from git.
# This flag causes pip to install the dependency locally, which is not what we want.
sed -i 's/^-e//g'
