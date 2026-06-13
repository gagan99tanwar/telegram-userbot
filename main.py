from telethon import TelegramClient, events
from telethon.sessions import StringSession
import random
import json
import os
import asyncio

# ================= TELEGRAM =================
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
STRING_SESSION = os.getenv("STRING_SESSION", "your_string_session")

# ✅ NO OTP MODE (ONLY STRING SESSION)
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# ================= GROUP =================
GROUP_USERNAME = "serien_gays"

# ================= DB =================
DB_FILE = "tg_ai_users.json"

db_lock = asyncio.Lock()

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

db = load_db()

# ================= USER =================
def get_user(uid):
    if uid not in db:
        db[uid] = {
            "name": None,
            "mood": "neutral",
            "anger": 0,
            "trust": 5,
            "affection": 0,
            "xp": 0,
            "level": 1,
            "memory": []
        }
    return db[uid]

def save_user(uid, user):
    db[uid] = user
    save_db(db)

# ================= MEMORY =================
def remember(user, msg):
    user["memory"] = (user["memory"] + [msg])[-20:]

# ================= EMOTION =================
def update_emotion(user, msg):
    msg = msg.lower()

    if "bot" in msg:
        user["anger"] += 1
        user["trust"] -= 1

    elif "sorry" in msg:
        user["anger"] = max(0, user["anger"] - 1)
        user["trust"] += 1

    elif "love" in msg or "like" in msg:
        user["affection"] += 1

    else:
        user["anger"] = max(0, user["anger"] - 0.05)

    user["anger"] = min(user["anger"], 5)
    user["trust"] = max(0, min(user["trust"], 10))
    user["affection"] = max(0, min(user["affection"], 10))

    if user["anger"] >= 4:
        user["mood"] = "savage"
    elif user["trust"] <= 2:
        user["mood"] = "cold"
    elif user["affection"] >= 7:
        user["mood"] = "friendly"
    else:
        user["mood"] = "neutral"

# ================= INTENT =================
def detect_intent(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hi", "hello", "hey"]):
        return "greet"
    if "love" in msg or "crush" in msg:
        return "love"
    if "study" in msg:
        return "study"
    if "friend" in msg or "yaar" in msg:
        return "friend"
    if "bot" in msg:
        return "bot"

    return "unknown"

# ================= RESPONSES =================
RESPONSES = {
    "greet": ["Hey 👋", "Hello 😄", "Kaise ho 😌", "Namaste 🙏"],
    "love": ["Pyaar complex hai ❤️‍🔥", "Feelings strong hoti hain 🫂"],
    "study": ["Padh lo 📚", "Focus karo 🔥"],
    "friend": ["Dosti priceless 🤝", "Main hamesha hu 🫂"],
    "bot": ["Main bot nahi hu 😤", "Insaan hu samjha 😡"]
}

FALLBACK = {
    "neutral": ["Acha 👀", "Samajh gaya 😌", "Interesting 🤔"],
    "savage": ["Bas karo 😤", "Time waste mat karo 😑"],
    "friendly": ["Nice 😄", "Good vibe ✨"],
    "cold": ["Hmm 😐", "Ok."]
}

# ================= BRAIN =================
def brain(user, intent):
    pool = RESPONSES.get(intent, FALLBACK[user["mood"]])
    reply = random.choice(pool)

    if user["trust"] > 7:
        reply += " 😌"
    if user["anger"] > 3:
        reply += " 😤"

    return reply

# ================= CORE =================
def get_reply(user_id, message):
    user = get_user(user_id)
    msg = message.lower()

    remember(user, msg)
    update_emotion(user, msg)

    intent = detect_intent(msg)

    if "my name is" in msg:
        name = msg.split("my name is")[-1].strip()
        user["name"] = name
        save_user(user_id, user)
        return f"Nice to meet you {name} 😄"

    if user["name"] and intent == "greet":
        reply = f"Hey {user['name']} 😌"
    else:
        reply = brain(user, intent)

    user["xp"] += 1
    if user["xp"] % 10 == 0:
        user["level"] += 1

    save_user(user_id, user)
    return reply

# ================= HANDLER =================
@client.on(events.NewMessage(chats=GROUP_USERNAME))
async def handler(event):
    if not event.raw_text:
        return

    # reply only when mentioned (stable behavior)
    if event.is_group and not event.mentioned:
        return

    user_id = str(event.sender_id)
    text = event.raw_text

    reply = get_reply(user_id, text)
    await event.reply(reply)

# ================= START =================
print("🤖 Bot running with StringSession (NO OTP MODE)")

client.start()
client.run_until_disconnected()
