#!/usr/bin/env bash

set -e

WORKSPACE_DIR=$(git rev-parse --show-toplevel)
cd "$WORKSPACE_DIR"

rm -r build
rm package.zip

pip install -r requirements.txt --target ./build

cp lambda_function.py build
cp -r src build
