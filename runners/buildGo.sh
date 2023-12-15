#!/usr/bin/env bash

set -e

TEMPFILE=$(mktemp)
go build -o "$TEMPFILE" "$1"
echo $TEMPFILE
