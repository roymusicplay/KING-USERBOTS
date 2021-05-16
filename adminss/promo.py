from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "promote"
__HELP__ = """
__**This command helps you to instantly promote someone in the chat**__
──「 **Usage** 」──
-> `promote`
"""

@kingbot.on_message(filters.group & filters.command("promote",vr.get("HNDLR")) & filters.user(Adminsettings))  
async def promotte(_, message):
    msg_id=message.message_id
    user_id=message.reply_to_message.from_user.id
    chat_id=message.chat.id
    can_promote=kingbot.get_chat_member(chat_id , message.user.id).can_promote_members
    user_info=kingbot.get_users(user_id)
    usercontact=None
    if(user_info.username):
        usercontact=user_info.username
    else:
        usercontact=user_info.first_name

    if(can_promote):
        chat_msg=message.text
        title=None
        if " " in chat_msg:
            space=chat_msg.index(" ")     
            chat_msg=str(chat_msg)
            title=chat_msg[space+1:len(chat_msg)]
        app.promote_chat_member(
            chat_id,
            user_id,
            can_manage_chat=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_manage_voice_chats=True,
            can_invite_users=True
        )
        if(title):
            kingbot.set_administrator_title(chat_id, user_id,title)
        if(user_info.username):
            usercontact=user_info.username
            reply_string="@"+usercontact+" has been promoted due to bribe"
            kingbot.edit_message_text(chat_id , msg_id , reply_string)
        else:
            usercontact=user_info.first_name
            reply_string=usercontact+" has been promoted due to bribe"
            kingbot.edit_message_text(chat_id , msg_id , reply_string)
    else:
        reply_string="Noob,you are not an admin !"
        reply_len=len(reply_string)
        for i in range(reply_len):
            edit_string=reply_string[0:i+2]
            try:
                kingbot.edit_message_text(chat_id , msg_id , edit_string )
            except:
                i=i+1
