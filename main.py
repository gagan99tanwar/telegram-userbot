from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import random
import asyncio

print("🚀 STABLE PRO BOT STARTING...")

# ENV VARIABLES
api_id = int(os.getenv("API_ID", "0"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TARGET_GROUP = "serien_gays"

# CHECK API KEY EARLY
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY MISSING IN RAILWAY VARIABLES")
else:
    print("✅ GEMINI API KEY LOADED")

# TELEGRAM CLIENT
client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

# GEMINI CALL (SAFE + FALLBACK SYSTEM)
def gemini(text):
    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    for model in models:
        try:
            print(f"🤖 Trying model: {model}")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

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

            print("STATUS:", r.status_code)

            if r.status_code != 200:
                print("ERROR RESPONSE:", r.text)
                continue

            data = r.json()

            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return reply

        except Exception as e:
            print(f"❌ Model {model} failed:", repr(e))
            continue

    return "😅 Sorry, abhi AI reply nahi de pa raha"

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

        # 50% reply chance
        if random.randint(1, 100) > 50:
            return

        print("\n📩 MESSAGE:", msg)

        # typing delay (human-like)
        await asyncio.sleep(random.randint(2, 6))

        reply = gemini(msg)

        print("💬 REPLY:", reply)

        await asyncio.sleep(random.randint(2, 5))

        await event.reply(reply)

    except Exception as e:
        print("❌ HANDLER ERROR:", repr(e))

print("✅ BOT INITIALIZING...")

client.start()

print("🔥 BOT RUNNING SUCCESSFULLY")

client.run_until_disconnected()
