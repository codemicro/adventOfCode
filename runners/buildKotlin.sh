#!/usr/bin/env bash

set -e

TEMPDIR="$(mktemp -d)"
FNAME=$(basename $1 | sed 's/\.kt$/.jar/')
FULLPATH="$TEMPDIR/$FNAME"
kotlinc "$1" -include-runtime -d "$FULLPATH"
echo $FULLPATH
