#!/bin/sh -e
cd "$(dirname "$(readlink -f "$0")")"
. venv/bin/activate
python src/main.py

