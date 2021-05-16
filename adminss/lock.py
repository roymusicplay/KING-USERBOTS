from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "lock"
__HELP__ = """
__**This command helps you to lock messages for non-admins in the chat**__
──「 **Usage** 」──
-> `lock`
"""

@kingbot.on_message(filters.command("lock",vr.get("HNDLR")) & filters.user(Adminsettings))  
def lock(_ , message):
    chat_id=message.chat.id
    can_lock=kingbot.get_chat_member(chat_id , "me").can_restrict_members
    if not can_lock:
        message.reply("Don't have enough permissions !!")
    else:
        message.reply("Chat has been locked for all non-admins !!")
        kingbot.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=False,
                can_invite_users=True
            )
        )