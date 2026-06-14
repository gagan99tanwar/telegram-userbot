from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import random
import asyncio

print("🚀 ULTRA PRO BOT STARTING...")

# =========================
# ENV VARIABLES
# =========================

api_id = int(os.getenv("API_ID", "0"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TARGET_GROUP = "serien_gays"

# Cooldown (seconds)
COOLDOWN = 30
last_reply_time = 0

# =========================
# CHECK VARIABLES
# =========================

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY NOT FOUND")
else:
    print("✅ GEMINI_API_KEY LOADED")

# =========================
# TELEGRAM CLIENT
# =========================

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

# =========================
# GEMINI FUNCTION
# =========================

def gemini(text):

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    prompt = f"""
You are chatting casually in a Telegram group.

Rules:
- Reply in natural Hinglish.
- Sound friendly and relaxed.
- Keep most replies short.
- Match the emotion of the user's message.
- If someone is happy, respond happily.
- If someone is sad, respond supportively.
- If someone is excited, show excitement too.
- If someone is joking, joke back naturally.
- If someone is angry, stay calm and friendly.
- Use emojis occasionally.
- Don't use bullet points.
- Don't sound like customer support.
- Don't over-explain.
- Talk like a normal group member.

User message:
{text}
"""

    for model in models:
        try:
            print(f"🤖 Trying model: {model}")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }

            r = requests.post(
                url,
                json=payload,
                timeout=20
            )

            print("STATUS:", r.status_code)

            if r.status_code != 200:
                print("ERROR:", r.text)
                continue

            data = r.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print("MODEL ERROR:", repr(e))
            continue

    return "😅"

# =========================
# MESSAGE HANDLER
# =========================

@client.on(events.NewMessage)
async def handler(event):
    global last_reply_time

    try:

        if not event.is_group:
            return

        if event.out:
            return

        chat = await event.get_chat()
        username = getattr(chat, "username", None)

        if username != TARGET_GROUP:
            return

        msg = event.raw_text.strip()

        if len(msg) < 2:
            return

        must_reply = False

        # Always reply when tagged
        if event.mentioned:
            must_reply = True

        # Always reply if someone replies to bot
        if event.is_reply:
            try:
                replied = await event.get_reply_message()

                if replied and replied.out:
                    must_reply = True
            except:
                pass

        now = asyncio.get_event_loop().time()

        # Cooldown only for random replies
        if not must_reply:
            if now - last_reply_time < COOLDOWN:
                return

            # 50% chance reply
            if random.randint(1, 100) > 50:
                return

        print("\n📩 MESSAGE:", msg)

        # Human delay
        await asyncio.sleep(random.randint(4, 12))

        reply = gemini(msg)

        if not reply:
            reply = "😄"

        print("💬 REPLY:", reply)

        await event.reply(reply)

        last_reply_time = now

    except Exception as e:
        print("❌ HANDLER ERROR:", repr(e))

# =========================
# START BOT
# =========================

print("✅ BOT INITIALIZING...")

client.start()

print("🔥 BOT RUNNING SUCCESSFULLY")

client.run_until_disconnected()
