#!/usr/bin/env bash

set -e

$(dirname $0)/build.sh
$(dirname $0)/package.sh
$(dirname $0)/upload.sh
