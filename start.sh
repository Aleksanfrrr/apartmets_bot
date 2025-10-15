#!/usr/bin/env bash
set -e

echo "== Show python-telegram-bot version =="
python - <<'PY'
import telegram
print("PTB version:", getattr(telegram, "__version__", "unknown"))
PY

echo "== Show first 60 lines of bot.py =="
nl -ba bot.py | sed -n '1,60p'

echo "== Install requirements =="
pip install --upgrade pip
pip install -r requirements.txt

echo "== RUN bot.py =="
python bot.py
