#!/usr/bin/env bash

set -e

WORKSPACE_DIR=$(git rev-parse --show-toplevel)
cd "$WORKSPACE_DIR"

aws lambda update-function-code \
    --function-name push_to_basecamp --zip-file fileb://package.zip --output text
