Telegram Video Access Bot
========================

Telegram Video Access Bot – bu bot foydalanuvchilarni belgilangan kanallarga obuna bo‘lishini tekshiradi va faqat to‘g‘ri obunachilarga videolarni yuboradi. Videolar Post ID yoki kod orqali qidirilishi mumkin.

Xususiyatlari
--------------
- Foydalanuvchi kanallarga obuna bo‘lganini tekshiradi.
- Owner kanalidan kelgan videolarni PostgreSQL bazasiga saqlaydi.
- Videolarni raqamli kod orqali qidirish va yuborish.
- Inline tugmalar orqali obuna bo‘lish va tekshirish funksiyasi.
- Ko‘p kanal va ko‘p owner qo‘llab-quvvatlanadi.

Talablar
--------
- Python 3.11+
- pyTelegramBotAPI
- psycopg2-binary
- python-dotenv
- PostgreSQL

O‘rnatish
----------
1. Repositoryni klonlash:  

    git clone https://github.com/username/telegram-video-bot.git
    cd telegram-video-bot

2. Virtual muhit yaratish va paketlarni o‘rnatish:  

    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

    pip install -r requirements.txt

3. `.env` faylini yaratish va sozlash:  

    TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
    PG_HOST=<POSTGRES_HOST>
    PG_DB=<POSTGRES_DB>
    PG_USER=<POSTGRES_USER>
    PG_PASSWORD=<POSTGRES_PASSWORD>
    PG_PORT=5432

    CHANNEL_USERNAME=channel1,channel2
    OWNER_CHANNEL=owner1,owner2

> Eslatma: Bir nechta kanallar yoki ownerlarni ',' bilan ajrating.

Foydalanish
-----------
1. Foydalanuvchi /start buyrug‘ini yuboradi.
2. Bot foydalanuvchi obunasini tekshiradi.
3. Agar foydalanuvchi barcha kanallarga obuna bo‘lgan bo‘lsa, video kodini yuborishi mumkin.
4. Agar kod topilsa, bot video va captionni yuboradi.
5. Agar kod topilmasa yoki foydalanuvchi obuna bo‘lmasa, bot inline tugmalar bilan kanalga obuna bo‘lishni so‘raydi.

Koddan misol
-------------
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

Ma’lumotlar bazasi (PostgreSQL)
--------------------------------
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    caption TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

Foydali havolalar
-----------------
- pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI
- psycopg2-binary: https://pypi.org/project/psycopg2-binary/
- Python dotenv: https://pypi.org/project/python-dotenv/

Litsenziya
----------
MIT License © 2025
