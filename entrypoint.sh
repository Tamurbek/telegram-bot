#!/bin/bash
set -e

# .env faylni yuklash (agar mavjud bo‘lsa)
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# DB tayyor bo‘lishini kutamiz
python wait_for_db.py

# Jadval yaratish
python create_tables.py

# Botni ishga tushiramiz
python bot.py