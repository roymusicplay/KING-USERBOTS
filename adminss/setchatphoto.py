from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "setchatphoto"
__HELP__ = """
__**This command helps you set chat photo **__
──「 **Usage** 」──
-> `setchatphoto`
"""

@kingbot.on_message(filters.group & filters.command("setchatphoto",vr.get("HNDLR")) & filters.user(Adminsettings))  
def set_chat_photo(_, message):
    msg_id=message.message_id
    chat_id=message.chat.id
    can_change_admin=kingbot.get_chat_member(chat_id , "me").can_change_info
    can_change_member=message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        message.reply("You don't have enough permission")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            kingbot.set_chat_photo(chat_id , photo=message.reply_to_message.photo.file_id)
            return
    else:
        message.reply("Reply to a photo to set it !")