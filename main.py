from telethon import TelegramClient, events
from telethon.sessions import StringSession
from replies import get_reply
import os
import random
import asyncio

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")

TARGET_GROUP = "serien_gays"  # apna group username

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

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

        # 70% chance reply
        if random.randint(1, 100) > 70:
            return

        msg = event.raw_text

        # Human-like delay
        await asyncio.sleep(random.randint(3, 10))

        reply = get_reply(msg)

        await event.reply(reply)

    except Exception as e:
        print("ERROR:", e)

print("BOT STARTED")

client.start()

print("BOT RUNNING...")

client.run_until_disconnected()
