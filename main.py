from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import sqlite3

# 🔐 ENV VARIABLES
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TARGET_GROUP = "serien_gays"

# 🚀 TELETHON CLIENT (FIXED SESSION)
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# 🗄️ SQLITE (RAILWAY SAFE)
conn = sqlite3.connect("/tmp/bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    message TEXT
)
""")
conn.commit()

# 🤖 GEMINI FUNCTION
def gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are a friendly Telegram assistant. Reply in Hinglish with attitude 😎\nUser: {text}"
            }]
        }]
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("Gemini Error:", e)
        return "😅 error aa gaya"

# 📩 MESSAGE HANDLER
@client.on(events.NewMessage)
async def handler(event):
    try:
        if not event.is_group:
            return

        chat = await event.get_chat()
        username = getattr(chat, "username", None)

        # ONLY TARGET GROUP
        if username != TARGET_GROUP:
            return

        msg = event.raw_text
        if not msg:
            return

        print("💬 Message:", msg)

        # SAVE TO DB
        cursor.execute(
            "INSERT INTO chats (user, message) VALUES (?, ?)",
            (str(event.sender_id), msg)
        )
        conn.commit()

        # GEMINI REPLY
        reply = gemini(msg)
        print("📤 Reply:", reply)

        await event.reply(reply)

    except Exception as e:
        print("Handler Error:", e)

# 🚀 START BOT
print("🔥 Bot Running...")
client.start()
client.run_until_disconnected()
