import re
import html
import aiohttp
from datetime import datetime
from asyncio import sleep
import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from kingbot import kingbot, vr , setbot, Adminsettings
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()



@kingbot.on_message(filters.command("song", vr.get("HNDLR")) & filters.user(Adminsettings))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    txt = message.text
    arg= txt.split(" ",1)[1]
    if arg is None:
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("Processing...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("Song not found.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit(f"Failed to download song due to Error: {ex}")
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await kingbot.send_chat_action(message.chat.id, "upload_audio")
    await kingbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
	
	
