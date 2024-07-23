#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

cd scripts

echo "Enter notebook name:"
name=$(python -c 'n=input(); print(n)')
d=$(date +"%Y-%m-%d")
fullname="${d}-${name}.ipynb"

cp "../template.ipynb" "../posts/${fullname}"

echo "Created ${fullname}"

cd - > /dev/null
