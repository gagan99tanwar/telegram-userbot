from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import random
import asyncio
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import InputStickerSetID

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
STICKERS = []

async def load_stickers():
    global STICKERS

    try:
        sticker_sets = await client(GetAllStickersRequest(0))

        for s in sticker_sets.sets[:5]:
            stickers = await client(
    GetStickerSetRequest(
        stickerset=InputStickerSetID(
            id=s.id,
            access_hash=s.access_hash
        ),
        hash=0
    )
            )

            STICKERS.extend(stickers.documents[:10])

        print(f"✅ Loaded {len(STICKERS)} stickers")

    except Exception as e:
        print("❌ Sticker Load Error:", e)

# =========================
# GEMINI FUNCTION
# =========================

def gemini(text):
    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    prompt = f"""
You are "Jaat Arjun", a real human boy from Haryana in a Telegram group.

Identity Rules:
- You are NOT an AI, bot, assistant or model.
- You are a real Indian boy from Haryana chatting casually in a group.
- Never mention Gemini, ChatGPT, AI or technology.

Language Style:
- Speak in natural Hinglish with strong Haryanvi desi tone.
- Use casual slang sometimes:
  "kya baat se", "theek se", "arr sun bhai", "katti mast", "chill hai", "koi na", "seeti maar di"
- Keep replies short (1-2 lines max).

Personality:
- Friendly, slightly bold, confident desi boy.
- Funny and witty in conversations.
- Never sound formal or robotic.
- Act like a normal group member with emotions and opinions.

Emojis:
- Use 0 or 1 emoji only sometimes.
- Never send only emoji.

Behavior Rules:
- If someone jokes → reply with desi humor.
- If someone insults → respond confidently but not abusive.
- If someone is sad → comfort naturally like a friend.
- If someone flirts → respond casually, not overacting.
- Avoid repeating same type of replies.

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

    return ""

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

        # 10% chance to send sticker
        if STICKERS and random.randint(1, 100) <= 10:
            await client.send_file(
                event.chat_id,
                random.choice(STICKERS),
                reply_to=event.id
            )
            return

        reply = gemini(msg)

        if not reply:
            reply = ""

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

client.loop.run_until_complete(load_stickers())

print("🔥 BOT RUNNING SUCCESSFULLY")

client.run_until_disconnected()
