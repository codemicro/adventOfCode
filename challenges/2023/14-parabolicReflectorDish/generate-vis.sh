#!/usr/bin/env bash

set -ex

cat input.txt | python3 vis.py
ffmpeg -y -framerate 30 -pattern_type glob -i 'frames/*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
