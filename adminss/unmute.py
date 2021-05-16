from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "unmute"
__HELP__ = """
__**This command helps you to unmute a user in the chat**__
──「 **Usage** 」──
-> `unmute`
"""

@kingbot.on_message(filters.group & filters.command("unmute",vr.get("HNDLR")) & filters.user(Adminsettings))  
def unmute(_, message):
    msg_id=message.message_id
    chat_msg=message.text
    username=None

    if "@" in chat_msg:
        index=chat_msg.index("@")     
        chat_msg=str(chat_msg)
        username=chat_msg[index+1:len(chat_msg)]
    else:                   
        username=message.reply_to_message.from_user.id

    chat_id=message.chat.id
    can_unmute=kingbot.get_chat_member(chat_id , "me").can_restrict_members
    user_info=kingbot.get_users(username)
    if(can_unmute):      
        kingbot.restrict_chat_member(chat_id , username , message.chat.permissions)
        if(user_info.username):
            usercontact=user_info.username
            reply_string="@"+usercontact+" has been released 😈"
            kingbot.edit_message_text(chat_id , msg_id , reply_string)
        else:
            usercontact=user_info.first_name
            reply_string=usercontact+" has been released 😈"
            kingbot.edit_message_text(chat_id , msg_id , reply_string)
    else:
        reply_string="Noob,you can't unmute members 😂 !"
        kingbot.edit_message_text(chat_id , msg_id , reply_string )