from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from kingbot import setbot, Adminsettings, kingbot, START_TIME , vr, vcbot
from datetime import datetime
import time
__MODULE__ = "alive"
__HELP__ = """
__**This command helps you to check wether userbot is alive**__
──「 **Usage** 」──
-> `alive`
"""
Alive_pic = "https://telegra.ph/file/040062841c541079a538c.jpg"
@kingbot.on_message(filters.user(Adminsettings) & filters.command("alive",vr.get("HNDLR")))
async def gooe_search(client, message):
    start_time = time.time()
    uptime = (datetime.now() - START_TIME)
    reply_msg = f"**KING USERBOT**"
    reply_msg += "------------------\n"
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    reply_msg += f"✔︎✔︎Ping: {ping_time}ms\n\n"
    reply_msg += f"𖣘𖣘Userbot uptime: {uptime}\n\n"
    reply_msg += f"☘︎☘︎__Running on pyrogram__☘︎☘︎\n"
    reply_msg += f"**ʕ•ᴥ•ʔPyhton versionʕ•ᴥ•ʔ**  : 3.8\n\n"
    reply_msg += f"( ͡° ͜ʖ ͡°)Servers functioning- normal♡´･ᴗ･`♡"
    await client.send_photo(message.chat.id , Alive_pic , reply_msg)
    await message.delete()
    if vcbot is not None:
        vcbot.send_message(message.chat.id, "Voice player alive")
