import os
import time
import telebot
from telebot import types
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

PG_HOST = os.getenv("PG_HOST", "db")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT", 5432)

CHANNELS = [f"@{os.getenv('CHANNEL_USERNAME')}"]
OWNER_CHANNEL = os.getenv("OWNER_CHANNEL")

def get_conn():
    return psycopg2.connect(
        host=PG_HOST,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
        port=PG_PORT
    )

def check_user(user_id):
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

@bot.channel_post_handler(content_types=["video"])
def handle_channel_post(message):
    # Faqat OWNER_CHANNEL dan kelgan postlarni saqlaymiz
    if message.chat.username == OWNER_CHANNEL:
        file_id = message.video.file_id
        caption = message.caption or ""
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO videos (file_id, caption) VALUES (%s, %s)",
                    (file_id, caption)
                )
        conn.close()

def ask_to_subscribe(chat_id):
    markup = types.InlineKeyboardMarkup()
    for ch in CHANNELS:
        markup.add(types.InlineKeyboardButton(text=ch, url=f"https://t.me/{ch[1:]}"))
    markup.add(types.InlineKeyboardButton("Tekshirish", callback_data="check"))
    bot.send_message(chat_id, "Botdan foydalanish uchun kanallarga obuna bo‘ling!", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_user(user_id):
        bot.send_message(message.chat.id, "Botdan foydalanishingiz mumkin!")
    else:
        ask_to_subscribe(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_callback(call):
    user_id = call.from_user.id
    if check_user(user_id):
        bot.send_message(call.message.chat.id, "Botdan foydalanishingiz mumkin!")
    else:
        bot.send_message(call.message.chat.id, "Hali barcha kanallarga obuna bo‘lmagansiz!")

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    user_id = message.from_user.id
    if not check_user(user_id):
        ask_to_subscribe(message.chat.id)
        return

    if message.text and message.text.isdigit():
        code = message.text
        conn = get_conn()
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT file_id, caption FROM videos")
                rows = cur.fetchall()
                for r in rows:
                    caption = r.get("caption") or ""
                    if f"Kod: {code}" in caption:
                        bot.send_video(message.chat.id, r["file_id"], caption=caption)
                        return
        conn.close()
        bot.send_message(message.chat.id, "Bu kod bo‘yicha video topilmadi.")
    else:
        bot.send_message(message.chat.id, "Kod faqat raqamlardan iborat bo‘lishi kerak!")

if __name__ == "__main__":
    # Botni ishga tushirishdan oldin Telegram token borligini tekshir
    if not TOKEN:
        raise RuntimeError("TOKEN muhit o‘zgaruvchisi topilmadi.")
    print("Bot ishga tushmoqda...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)