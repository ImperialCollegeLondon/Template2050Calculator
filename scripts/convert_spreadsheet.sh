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

docker run --pull always --rm -it -u "$(id -u)":"$(id -g)" \
       -v "${spreadsheet}":/opt/excel_to_code/input.xlsx:ro \
       -v "$(pwd)":/opt/excel_to_code/work/ \
       ghcr.io/imperialcollegelondon/calc2050_excel_to_code:main \
       bash ./run.sh

cp model/_interface2050.cpython-39-x86_64-linux-gnu.so model/interface2050.py server_code/
