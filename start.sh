#!/usr/bin/env bash
set -e

pip install --upgrade pip
pip uninstall -y python-telegram-bot || true
pip install --no-cache-dir -r requirements.txt

python bot.py
