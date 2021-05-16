from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "block"
__HELP__ = """
__**This command helps you to block a user in pm**__
──「 **Usage** 」──
-> `block`
"""

@kingbot.on_message(filters.command("block",vr.get("HNDLR")) & filters.user(Adminsettings))  
async def block_user(_, message):
    if not message.chat.type == "private":
        await message.reply("Can't block the group LOL !")
    else:
        user_id=message.chat.id
        await message.reply("You have been blocked succesfully due to your sins !!")
        await client.block_user(user_id)
