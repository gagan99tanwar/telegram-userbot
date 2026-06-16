from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import random
import asyncio
import time
from collections import deque

from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import InputStickerSetID

print("🚀 ULTRA HUMAN USERBOT STARTING...")

# =========================
# ENV
# =========================

api_id = int(os.getenv("API_ID", "0"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")

GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
    os.getenv("GEMINI_API_KEY_6"),
]

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

# =========================
# DATA STORAGE
# =========================

STICKERS = []
MESSAGE_BUFFER = {}
USER_LAST_REPLY = {}

COOLDOWN = 3

# =========================
# STICKER SYSTEM (FULL FIX)
# =========================

async def load_stickers():
    global STICKERS
    try:
        sets = await client(GetAllStickersRequest(0))

        for s in sets.sets[:3]:
            pack = await client(
                GetStickerSetRequest(
                    stickerset=InputStickerSetID(id=s.id, access_hash=s.access_hash),
                    hash=0
                )
            )
            STICKERS.extend(pack.documents[:15])

        print(f"✅ Stickers Loaded: {len(STICKERS)}")

    except Exception as e:
        print("Sticker Error:", e)

async def send_random_sticker(chat_id):
    if not STICKERS:
        return

    try:
        if random.randint(1, 4) == 1:  # 25% chance
            sticker = random.choice(STICKERS)
            await client.send_file(chat_id, sticker)
    except:
        pass

# =========================
# KEY ROTATION
# =========================

key_status = {k: "active" for k in GEMINI_KEYS if k}
key_index = 0

def get_next_key():
    global key_index
    keys = list(key_status.keys())

    if not keys:
        return None

    for _ in range(len(keys)):
        key = keys[key_index % len(keys)]
        key_index += 1
        if key_status.get(key) == "active":
            return key
    return None

def mark_bad(key):
    key_status[key] = "cooldown"

# =========================
# GEMINI (HUMAN THINKING ENGINE)
# =========================

def gemini(text):
    models = ["gemini-2.5-flash", "gemini-2.0-flash"]

    prompt = f"""
You are a real Indian Gen-Z boy in Telegram group.

RULES:
- Treat everyone as male friends.
- Only reply when spoken to directly or relevant.
- Never interrupt others' conversations.
- If someone says hi/hello → reply casually hi back.
- If tagged or replied → respond properly.
- Understand message context before replying.
- Keep reply short (1-2 lines).
- Natural Hinglish only.

Message:
{text}
"""

    for model in models:
        key = get_next_key()
        if not key:
            return None

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

            r = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}]
            }, timeout=15)

            if r.status_code in [403, 429]:
                mark_bad(key)
                continue

            if r.status_code != 200:
                continue

            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except:
            mark_bad(key)

    return None

# =========================
# SMART BUFFER (ANTI-SPAM + HUMAN BEHAVIOR)
# =========================

async def process_user(uid):
    await asyncio.sleep(2.5)

    if uid not in MESSAGE_BUFFER:
        return

    event, _ = MESSAGE_BUFFER[uid][-1]
    MESSAGE_BUFFER[uid].clear()

    await handle_event(event)

# =========================
# MAIN LOGIC
# =========================

async def handle_event(event):
    uid = event.sender_id
    msg = event.raw_text or ""
    now = time.time()

    # cooldown per user
    if uid in USER_LAST_REPLY:
        if now - USER_LAST_REPLY[uid] < COOLDOWN:
            return

    reply = gemini(msg)

    if not reply:
        return

    typing_time = min(max(len(reply) / 18, 1.2), 3.0)

    async with client.action(event.chat_id, "typing"):
        await asyncio.sleep(typing_time)
        await event.reply(reply)

    USER_LAST_REPLY[uid] = now

    # sticker sometimes
    await send_random_sticker(event.chat_id)

# =========================
# HUMAN BEHAVIOR HANDLER
# =========================

@client.on(events.NewMessage)
async def handler(event):

    if event.out:
        return

    msg = event.raw_text or ""
    if len(msg) < 2:
        return

    uid = event.sender_id

    # buffer system (no message loss)
    if uid not in MESSAGE_BUFFER:
        MESSAGE_BUFFER[uid] = []

    MESSAGE_BUFFER[uid].append((event, time.time()))

    asyncio.create_task(process_user(uid))

# =========================
# START
# =========================

client.start()
client.loop.create_task(load_stickers())

print("🔥 ULTRA HUMAN MODE ACTIVE (MEMBER-LIKE BEHAVIOR + STICKERS)")
client.run_until_disconnected()
