from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os

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

def gemini(text):
    print("USING GEMINI")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Reply naturally in Hinglish. User message: {text}"
                        }
                    ]
                }
            ]
        }

        r = requests.post(url, json=payload, timeout=20)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

        if r.status_code != 200:
            return f"API Error {r.status_code}"

        data = r.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return "😅 error aa gaya"

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

        print("MESSAGE EVENT TRIGGERED")
        print("MESSAGE:", msg)

        reply = gemini(msg)

        print("REPLY:", reply)

        await event.reply(reply)

    except Exception as e:
        print("HANDLER ERROR:", repr(e))

print("BOT STARTED")

client.start()

print("BOT RUNNING...")

client.run_until_disconnected()
