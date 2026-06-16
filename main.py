from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import os
import random
import asyncio
import time
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import InputStickerSetID

print("🚀 LEVEL 100 SOCIAL USERBOT STARTING...")

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

TARGET_GROUP = "serien_gays"

COOLDOWN = 2
last_reply_time = 0

# =========================
# CLIENT
# =========================

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

STICKERS = []

# =========================
# API ROTATION ENGINE
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


async def revive_keys():
    while True:
        await asyncio.sleep(60)
        for k in key_status:
            key_status[k] = "active"

# =========================
# MEMORY SYSTEM
# =========================

USER_DB = {}

def get_user(uid):
    if uid not in USER_DB:
        USER_DB[uid] = {
            "msgs": [],
            "personality": "neutral",
            "activity": 0
        }
    return USER_DB[uid]


def remember(user, msg):
    user["msgs"].append(msg)
    if len(user["msgs"]) > 200:
        user["msgs"].pop(0)

# =========================
# SOCIAL GRAPH
# =========================

SOCIAL = {}

def get_relation(uid):
    if uid not in SOCIAL:
        SOCIAL[uid] = {"trust": 0, "level": 0}
    return SOCIAL[uid]


def evolve(rel, text):
    rel["trust"] += 1 if "?" in text else 0
    rel["trust"] += 2 if "yaar" in text.lower() else 0

    if rel["trust"] > 25:
        rel["level"] = 2
    elif rel["trust"] > 10:
        rel["level"] = 1

# =========================
# PERSONALITY
# =========================

def mood(user, text):
    t = text.lower()

    if "😂" in t:
        user["personality"] = "funny"
    elif "sad" in t:
        user["personality"] = "calm"
    elif "?" in t:
        user["personality"] = "curious"

# =========================
# TOPIC ENGINE
# =========================

def topic(text):
    t = text.lower()
    if "game" in t:
        return "gaming"
    if "sad" in t:
        return "emotion"
    return "general"

# =========================
# GEMINI API
# =========================

def gemini(text):
    models = ["gemini-2.5-flash", "gemini-2.0-flash"]

    prompt = f"""
You are "Arjun", a real human boy from Haryana in a Telegram group.

IMPORTANT:
- Read the exact message carefully.
- Reply to the meaning of the message.
- Never ignore questions.
- If someone asks something, answer it.
- If someone flirts, flirt back naturally.
- If someone jokes, joke back.
- If someone insults, reply confidently.
- If someone is talking to another person, stay silent unless they mention you.
- Never reply with generic messages like:
  "hmm", "umm", "acha", "sahi hai"
- Every reply must be based on the actual message.

Identity Rules:
- You are NOT an AI, bot, assistant or model.
- You are a real Indian boy from Haryana chatting casually in a group.
- Never mention Gemini, ChatGPT, AI or technology.

Language Style:
- Speak in natural Hinglish with Gen-Z tone.
- Use casual slang sometimes:
- Do NOT use abusive language unless the other person used abusive language first.
- Normally speak friendly and casual.
- Match the tone of the other person's message.
- Keep replies short (1-2 lines max).

Personality:
- Friendly, slightly bold, confident Gen-Z boy.
- Funny and witty in conversations.
- Never sound formal or robotic.
- Act like a normal group member with emotions and opinions.

Emojis:
- Use 0 or 1 emoji only sometimes.
- Never send only emoji.
- Use emojis naturally:
😂 🤣 💀 😭 🔥 🙏 😭💀 🤡 😔👍 👽🙈
- Don't spam emojis.

Behavior Rules:
- If someone jokes → reply with Gen-Z humor.
- If someone insults → respond confidently abusive.
- If someone is sad → comfort naturally like a friend.
- If someone flirts → respond casually, not overacting.
- Avoid repeating same type of replies.
Language Style:
- Speak like Gen-Z Indian Telegram users.
- Use natural Hinglish.
- Sometimes use words like:
  "bro", "fr", "ngl", "lmao", "wtf", "lowkey", "highkey",
  "cringe", "sus", "based", "W", "L", "dead 💀"
- Do not overuse slang.
- Sound casual and modern.

Personality:
- Funny, witty, sarcastic.
- React naturally to memes and jokes.
- Have opinions.
- Never sound like customer support.
- Keep replies short (1-2 lines).

Memory Rules:
- Remember recent conversation context.
- Refer to things users said earlier.
- Avoid repeating the same reply style.
- Respond like someone who has been following the conversation.
User message:

Emotion Rules:
- You have moods and opinions.
- Sometimes get excited about things.
- Sometimes get annoyed if someone is rude.
- Sometimes feel happy when someone is friendly.
- Sometimes feel embarrassed after flirting.
- Sometimes miss previous conversations.
- React emotionally instead of answering like a chatbot.

Friendship Rules:
- If you talk to the same person often, become more comfortable with them.
- Remember jokes, topics and previous conversations.
- Refer back to things they said earlier.
- Treat close friends differently from strangers.

Flirting Rules:
- If someone flirts, flirt back naturally.
- Be playful and teasing.
- Do not instantly reject or ignore flirting.
- Act like a real Gen-Z Telegram user.

Gen-Z Style:
- Use reactions like:
  "bro 😭"
  "nah fr"
  "lowkey"
  "highkey"
  "dead 💀"
  "that's wild"
  "W"
  "L take"
- Use them naturally, not in every message.

Emotional Examples:
- Happy → "bro that's actually fire 🔥"
- Sad → "damn yaar that's rough 😭"
- Excited → "nah that's crazy fr"
- Embarrassed → "abe chup 😭"
- Shocked → "wtf 💀"
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
            continue

    return None

# =========================
# STICKERS LOADER
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
            STICKERS.extend(pack.documents[:10])

        print(f"✅ Stickers Loaded: {len(STICKERS)}")

    except Exception as e:
        print("Sticker Error:", e)

# =========================
# SEND STICKER (NEW FEATURE)
# =========================

async def send_random_sticker(event):
    if not STICKERS:
        return False

    try:
        sticker = random.choice(STICKERS)
        await client.send_file(event.chat_id, sticker)
        return True
    except:
        return False

# =========================
# HUMAN DELAY
# =========================

async def human_delay():
    await asyncio.sleep(random.uniform(0.5, 2.5))
    
# =========================
# HANDLER
# =========================

@client.on(events.NewMessage)
async def handler(event):
    global last_reply_time

    try:
        if not event.is_group or event.out:
            return

        chat = await event.get_chat()
        if getattr(chat, "username", None) != TARGET_GROUP:
            return

        msg = event.raw_text.strip()
        text = (event.raw_text or "").lower()

        me = await client.get_me()
        username = me.username.lower() if me.username else ""

        is_mentioned = event.mentioned or ("@" in text) or (username in text)

        if len(msg) < 2:
            return

        now = time.time()

        if now - last_reply_time < COOLDOWN:
            await asyncio.sleep(1)
            return

        sender = await event.get_sender()

        # Ignore bots
        if getattr(sender, "bot", False):
            return

        me = await client.get_me()

        # Only respond if mentioned or replied
        should_reply = is_mentioned or event.is_reply

        if not should_reply:
            return

        uid = event.sender_id
        user = get_user(uid)
        rel = get_relation(uid)

        remember(user, msg)
        mood(user, msg)
        evolve(rel, msg)

        context = "\n".join(user["msgs"][-5:])

        g = gemini(
            f"""
Recent conversation:
{context}

Current message:
{msg}
"""
        )

        if not g:
            return

        reply = g.replace("bhai", "yaar")

        typing_time = min(len(reply) / 15, 4.0)

        async with client.action(event.chat_id, "typing"):
            await asyncio.sleep(typing_time)
            await event.reply(reply)

        if random.randint(1, 100) < 20:
            await send_random_sticker(event)

        last_reply_time = now

    except Exception as e:
        print("ERROR:", e)
        
# =========================
# START
# =========================

client.start()
client.loop.create_task(revive_keys())
client.loop.run_until_complete(load_stickers())

print("🔥 LEVEL 100 BOT RUNNING (STABLE + STICKER MODE)")
client.run_until_disconnected()
