from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "unlock"
__HELP__ = """
__**This command helps you to unlock chat for non-admins in the chat**__
──「 **Usage** 」──
-> `unlock`
"""

@kingbot.on_message(filters.command("unlock",vr.get("HNDLR")) & filters.user(Adminsettings))
def unlock(_, message):
    chat_id=message.chat.id
    message.reply("Chat has been unlocked !!")
    kingbot.set_chat_permissions(
        chat_id,
        ChatPermissions(
            can_send_messages=True,
            can_send_stickers=True,
            can_send_media_messages=True,
            can_send_animations=True
        )
    )  