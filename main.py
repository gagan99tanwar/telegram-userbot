from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import random
import asyncio

print("VERSION TEST 999")

# ENV VARIABLES
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TARGET_GROUP = "serien_gays"

# TELEGRAM CLIENT
client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

# GEMINI FUNCTION (2.5 FLASH)
def gemini(text):
    print("USING GEMINI 2.5 FLASH")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Reply naturally in Hinglish like a human. User message: {text}"
                        }
                    ]
                }
            ]
        }

        r = requests.post(url, json=payload, timeout=20)

        if r.status_code != 200:
            print("STATUS:", r.status_code, r.text)
            return f"API Error {r.status_code}"

        data = r.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return "😅 error aa gaya"

# MESSAGE HANDLER
@client.on(events.NewMessage)
async def handler(event):
    try:
        if not event.is_group:
            return

        if event.out:
            return

        chat = await event.get_chat()
        username = getattr(chat, "username", None)

        if username != TARGET_GROUP:
            return

        msg = event.raw_text

        # 50% chance reply
        if random.randint(1, 100) > 50:
            return

        print("MESSAGE:", msg)

        # Gemini reply
        reply = gemini(msg)

        # human-like delay
        await asyncio.sleep(random.randint(3, 10))

        print("REPLY:", reply)

        # fallback
        if not reply:
            reply = "😄"

        await event.reply(reply)

    except Exception as e:
        print("HANDLER ERROR:", repr(e))

print("BOT STARTED")

client.start()

print("BOT RUNNING...")

client.run_until_disconnected()
