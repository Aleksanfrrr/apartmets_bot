#!/usr/bin/env bash
set -e

echo "=== CLEAN INSTALL START ==="
pip uninstall -y python-telegram-bot || true
pip install --no-cache-dir python-telegram-bot==20.8

echo "=== MARKER: start.sh v4 ==="
python -c "import telegram; print('PTB version =', telegram.__version__)"
echo "== RUN bot.py =="
python bot.py
