from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "mute"
__HELP__ = """
__**This command helps you to mute a user in the chat**__
──「 **Usage** 」──
-> `mute`
"""

@kingbot.on_message(filters.command("mute",vr.get("HNDLR")) & filters.user(Adminsettings))  
def mute(_, message):
    
    msg_id=message.message_id
    chat_id=message.chat.id
    can_mute=kingbot.get_chat_member(chat_id , "me").can_restrict_members
    chat_msg=message.text
    
    user_id=None
    if "@" in chat_msg:
        index=chat_msg.index("@")     
        chat_msg=str(chat_msg)
        user_id=chat_msg[index+1:len(chat_msg)]
    else:                   
        user_id=message.reply_to_message.from_user.id
    user_info=kingbot.get_users(user_id)
    can_user_ban=kingbot.get_chat_member(chat_id , user_id).can_restrict_members

    if(can_mute):
        if(can_user_ban):
            reply_string="Can't mute another admin. LOL !"
            kingbot.edit_message_text(chat_id , msg_id , reply_string )
        else:            

            kingbot.restrict_chat_member(chat_id , user_id , ChatPermissions() , int(time()+86400))
            if(user_info.username):
                usercontact=user_info.username
                reply_string="@"+usercontact+" has been muted for 24hrs !"
                kingbot.edit_message_text(chat_id , msg_id , reply_string)
            else:
                usercontact=user_info.first_name
                reply_string=usercontact+" has been muted for 24hrs !"
                kingbot.edit_message_text(chat_id , msg_id , reply_string)
    else:
        reply_string="Noob,you can't mute members 😂 !"
        kingbot.edit_message_text(chat_id , msg_id , reply_string )

