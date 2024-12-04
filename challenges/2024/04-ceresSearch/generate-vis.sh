#!/usr/bin/env bash

set -ex

cat input.txt | PYTHONPATH=../../../ python3 vis.py
