from pyrogram import client, filters
import asyncio
import time
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "setvar"
__HELP__ = """
__**This command helps you to set var**__
──「 **Usage** 」──
-> `setvar`
"""
Vari=["HNDLR","VC_SESSION", "VC_API_ID" ,"VC_API_HASH"]
@kingbot.on_message(filters.group & filters.command("setvar",vr.get("HNDLR")) & filters.user(Adminsettings))  
async def varistr(_, message):
  msg_txt=message.text
  if " " in msg_txt:
        await message.edit_text("getting vars from message")
        content=msg_txt.split(" " ,1)[1]
        keyy= content.split(" ", 1)[0]
        valuee = content.split(" ",1)[1]
        await message.edit_text("separating the vars")
        if keyy == "VC_SESSION":
             if vr.get("VC_API_ID") is None & vr.get("VC_API_HASH") is None:
                     await message.edit_text("First set `VC_API_HASH` and `VC_API_ID` to use music. Then set the VC_SESSION")
                     return
             else:
                     pass
        if keyy== "VC_API_ID":
              keyy = int(valuee)
        try:
           await vr.set(keyy , valuee)
           await message.edit_text("The var has been set\n Restart the app to enjoy")
        except Exception as err:
           await message.reply_text("error")
           await message.edit_text(f"Encountered a error:{str(err)}")
