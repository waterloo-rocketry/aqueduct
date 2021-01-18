#!/usr/bin/env bash

set -e

warn_windows () {
    echo "Command-line packaging is not supported on Windows."
    echo "Please use 7-Zip or other packaging software."
    exit 1
}

case "$OSTYPE" in
    linux*)  zip package.zip build ;;
    msys*)   warn_windows ;;
esac
