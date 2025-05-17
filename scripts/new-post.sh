#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

echo "Enter notebook name:"
name=$(uv run python -c 'n=input(); print(n)')
d=$(date +"%Y-%m-%d")
fullname="posts/${d}-${name}.ipynb"

cp "post-template.ipynb" "${fullname}"

echo "Created ${fullname}"

uv run jupyter lab --browser=google-chrome --notebook-dir=posts "${fullname}"
