from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "unpin"
__HELP__ = """
__**This command helps you to instantly unpin a message in the chat**__
──「 **Usage** 」──
-> `unpin`
"""

@kingbot.on_message(filters.command("unpin",vr.get("HNDLR")) & filters.user(Adminsettings))  
def unpin_message(_, message):
    msg_id=message.message_id
    chat_id=message.chat.id
    if message.reply_to_message == None:
        kingbot.edit_message_text(chat_id , msg_id , "Shall I unpin your head from wall ?")
    else:
        if message.chat.type == "private":
            client.unpin_chat_message(chat_id , msg_id , both_sides=True)
            kingbot.edit_message_text(chat_id , msg_id , "Done the Job master !")
        else:
            can_pin=kingbot.get_chat_member(chat_id , "me").can_pin_messages
            if can_pin == None:
                kingbot.edit_message_text(chat_id , msg_id , "Can't pin messages bruh 🥱") 
            else:         
                reply_msg_id=message.reply_to_message.message_id
                client.unpin_chat_message(chat_id , reply_msg_id)
                kingbot.edit_message_text(chat_id , msg_id , "Done the Job master !")
