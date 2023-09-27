#!/bin/sh

cd "$(dirname "$(readlink -f "$0")")"

create_activate_venv() {
    [ -d "$1" ] && python -m venv "$1"
    . "${1}/bin/activate"
}
create_activate_venv venv

pip install -r requirements.txt

python src/main.py

