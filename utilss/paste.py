from pyrogram import client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions
from kingbot import kingbot, vr ,Adminsettings
__MODULE__ = "paste"
__HELP__ = """
__**This command helps you to paste a text to nekobin.com and return a shareable url**__
──「 **Usage** 」──
-> `paste`
"""

@kingbot.on_message(filters.command("paste",vr.get("HNDLR")) & filters.user(Adminsettings))  
async def paste(_,message):
   msg_txt=message.text
   if msg_txt:
    if " " in msg_txt:
        content=msg_txt[msg_txt.index(" ")+1:len(msg_txt)]
        req = requests.post('https://nekobin.com./api/documents',json={"content":content})
        key = json.loads(req.content)["result"]["key"]
        await message.reply(f"Nekofied to https://nekobin.com/{key}")
    else:
        if message.reply_to_message:
            if message.reply_to_message.text:
                content=message.reply_to_message.text
                req = requests.post('https://nekobin.com./api/documents',json={"content":content})
                key = json.loads(req.content)["result"]["key"]
                await message.reply(f"Nekofied to https://nekobin.com/{key}")
            else:
                await message.reply("Can only paste text LOL !")
        else:
            await message.reply("Give me something to paste !")    
   if not msg_txt:
        if not message.reply_to_message:
            await message.edit_text("`Reply To File / Give Me Text To Paste!`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            content = m_list
            os.remove(file)
            req = requests.post('https://nekobin.com./api/documents',json={"content":content})
            key = json.loads(req.content)["result"]["key"]
            await message.reply(f"Nekofied to https://nekobin.com/{key}")
