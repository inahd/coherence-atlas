#!/usr/bin/env bash

cd /opt/atlas
source venv/bin/activate

case "$1" in

run)
    python atlas/ui/main_menu.py
    ;;

push)
    git add .
    git commit -m "Atlas cycle update"
    git push
    ;;

status)
    git status
    ;;

scan)
    python scripts/doctor.py
    ;;

*)
    echo "Atlas commands:"
    echo "  ./run.sh run     - launch atlas"
    echo "  ./run.sh push    - commit + push"
    echo "  ./run.sh status  - git status"
    echo "  ./run.sh scan    - integrity check"
    ;;

esac
