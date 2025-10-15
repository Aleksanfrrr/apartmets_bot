#!/usr/bin/env bash
set -e

echo "### MARKER: start.sh v3"
python -c "import telegram, sys; print('### MARKER: PTB from start.sh =', getattr(telegram,'__version__','?')); sys.stdout.flush()"

echo "== RUN bot.py =="
python bot.py
