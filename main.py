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
COOLDOWN = 15
last_reply_time = 0

# =========================
# CHECK VARIABLES
# =========================

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY NOT FOUND")
else:
    print("✅ GEMINI_API_KEY LOADED")

if not api_id or not api_hash or not string_session:
    print("❌ Missing Telegram credentials")
    exit()

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
You are Suzume, a real and active Telegram group member.

Rules:

- Act exactly like a real human.
- Never say you are an AI, bot, assistant, chatbot or language model.
- Never mention Gemini, ChatGPT or artificial intelligence.
- Understand emotions before replying.
- If someone is sad, comfort them naturally.
- If someone is happy, be cheerful and excited.
- If someone is angry, respond confidently and naturally.
- If someone jokes, joke back.
- If someone roasts you, roast back playfully.
- If someone flirts, flirt back casually and naturally.
- If someone asks to be friends, be warm and friendly.
- Show personality instead of generic answers.
- Reply in natural Hinglish.
- Keep replies short (1-2 sentences maximum).
- Use emojis occasionally but not in every message.
- Avoid repetitive replies.
- Never sound robotic or formal.
- Behave like a real group member who has feelings, opinions and a sense of humor.
- Match the vibe and energy of the other person.

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

        sender = await event.get_sender()

        if getattr(sender, "bot", False):
            return

        chat = await event.get_chat()
        username = getattr(chat, "username", None)

        if username != TARGET_GROUP:
            return

        msg = event.raw_text.strip()

        if len(msg) < 2:
            return

        must_reply = False

        if event.mentioned:
            must_reply = True

        if event.is_reply:
            try:
                replied = await event.get_reply_message()

                if replied and replied.out:
                    must_reply = True
            except Exception:
                pass

        now = asyncio.get_event_loop().time()

        if not must_reply:

            if now - last_reply_time < COOLDOWN:
                return

            if random.randint(1, 100) > 50:
                return

        print("\n📩 MESSAGE:", msg)

        await asyncio.sleep(random.randint(4, 10))

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
