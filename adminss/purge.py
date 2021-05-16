from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "purge"
__HELP__ = """
__**This command helps you to delete all messages from a replied message in the chat**__
──「 **Usage** 」──
-> `purge`
"""

@kingbot.on_message(filters.command("purge",vr.get("HNDLR")) & filters.user(Adminsettings))  
def purge(_, message):
    chat_id=message.chat.id
    if message.reply_to_message:
        if message.chat.type == "group":
            reply_msg_id=message.reply_to_message.message_id
            current_msg_id=message.message_id
            can_delete=kingbot.get_chat_member(chat_id , "me").can_delete_messages
            if can_delete:
                for msg_id in range(reply_msg_id , current_msg_id ,1):
                    client.delete_messages(chat_id , msg_id)
                message.reply("All messages purged , no hint left !")
            else:
                message.reply("Mistakes can't be deleted by everyone !")
        else:
            reply_msg_id=message.reply_to_message.message_id
            current_msg_id=message.message_id
            for msg_id in range(reply_msg_id , current_msg_id ,1):
                    kingbot.delete_messages(chat_id , msg_id)
            message.reply("All messages purged , no hint left !")
    else:
        message.reply("Shall I delete your existence ?😌")
