from telethon import TelegramClient, events
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["STRING_SESSION"]

client = TelegramClient(session, api_id, api_hash)

@client.on(events.NewMessage)
async def auto_reply(event):
    if event.is_group and not event.out:
        await event.reply("I'm currently offline.")

client.start()
print("Userbot Started")
client.run_until_disconnected()
