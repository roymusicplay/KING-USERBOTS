import re
from datetime import datetime
from asyncio import sleep
import os
import time
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
from kingbot import kingbot, vr , setbot, Adminsettings
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message
from urllib.request import urlretrieve
import requests as r
import wget
from utilss.paste import get_text
__MODULE__ = "Song"
__HELP__ = """
__**This command helps you to download and send songs to a chat**__
──「 **Usage** 」──
-> `song name`
"""

@kingbot.on_message(filters.command("song", vr.get("HNDLR")) & filters.user(Adminsettings))
async def song(client, message):
    input_str = get_text(message)
    rep= await message.edit_text(f"`Processing...`")
    if not input_str:
        await rep.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    await rep.edit(f"`Getting {input_str} From Youtube Servers. Please Wait.`")
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    result_s = rt["search_result"]
    url = result_s[0]["link"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await rep.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_sung= f"{ytdl_data['id']}.mp3"
    capy = f"**Song Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    await client.send_audio(
        message.chat.id,
        audio=open(file_sung, "rb"),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=downloaded_thumb,
        caption=capy,
        supports_streaming=True,
    )
    await rep.delete()
    for files in (downloaded_thumb, file_sung):
        if files and os.path.exists(files):
            os.remove(files)
            
	
	
@kingbot.on_message(filters.command("saavan", vr.get("HNDLR")) & filters.user(Adminsettings))
async def savnana(client, message):
    song = get_text(message)
    if not song:
        return await message.edit_text("`Give me Something to Search")
    hmm = time.time()
    lol = await message.edit_text("`Searching on Saavn...`")
    sung = song.replace(" ", "%20")
    url = f"https://jostapi.herokuapp.com/saavn?query={sung}"
    try:
        k = (r.get(url)).json()[0]
    except IndexError:
        return await eod(lol, "`Song Not Found.. `")
    title = k["song"]
    urrl = k["media_url"]
    img = k["image"]
    duration = k["duration"]
    singers = k["singers"]
    urlretrieve(urrl, title + ".mp3")
    urlretrieve(img, title + ".jpg")
    file= await wget.download(urrl)
    await client.send_audio(message.chat.id,file,caption=f"Song from saavan uploaded by king Userbot \n Song name={title}\n Singers={singers}" )   
    await lol.delete()
    os.remove(title + ".mp3")
    os.remove(title + ".jpg")
