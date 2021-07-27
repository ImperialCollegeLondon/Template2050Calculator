#!/bin/sh

set -euo pipefail

realpath() {
    # macOS doesn't have realpath by default so stole this
    # https://stackoverflow.com/questions/3572030/bash-script-absolute-path-with-os-x/3572105#3572105
    OURPWD=$PWD
    cd "$(dirname "$1")"
    LINK=$(readlink "$(basename "$1")")
    while [ "$LINK" ]; do
	cd "$(dirname "$LINK")"
	LINK=$(readlink "$(basename "$1")")
    done
    REALPATH="$PWD/$(basename "$1")"
    cd "$OURPWD"
    echo "$REALPATH"
}

spreadsheet=$(realpath "$1")

docker run --pull always -u "$(id -u)":"$(id -g)" --rm -it \
       -v "${spreadsheet}":/input.xlsx -v "$(pwd)":/work \
       --workdir /work ghcr.io/imperialcollegelondon/calc2050_get_weboutputs:latest \
       python /get_weboutputs.py /input.xlsx
