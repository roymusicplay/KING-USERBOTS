from queue import Queue, Empty
from typing import Dict, Union
from youtube_dl import YoutubeDL
from os import path
import asyncio
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message, Chat, User, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from uti.errors import FFmpegReturnCodeError
from typing import List, Dict, Union,Callable, Coroutine
from kingbot import vcbot, setbot , Adminsettings
from youtubesearchpython import VideosSearch
__MODULE__ = "Voice Chat Player"
__HELP__="""
The commands and there use is explained here-: 
 `/play` Reply this in response to a link or any telegram audio file it will be played 
 `/skip` to skip current song
 `/stop` or `/kill` to stop the streaming of song 
 `/pause` to pause the stream 
 `/resume` to resume the playback. 
 Inline search is also supported.
"""
queues: Dict[int, Queue] = {}


def add(chat_id: int, file_path: str) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()

    queues[chat_id].put({"file_path": file_path})
    return queues[chat_id].qsize()


def get(chat_id: int) -> Union[Dict[str, str], None]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return None


def is_empty(chat_id: int) -> Union[bool, None]:
    if chat_id in queues:
        return queues[chat_id].empty()
    else:
        return True


def task_done(chat_id: int) -> None:
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass


def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].queue = []
    else:
        raise Empty

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    ydl.download([url])


async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 1 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    if proc.returncode != 0:
        raise FFmpegReturnCodeError("FFmpeg did not return 0")

    return out

admins: Dict[str, List[User]] = {}

def set(chat_id: Union[str, int], admins_: List[User]):
    if isinstance(chat_id, int):
        chat_id = str(chat_id)

    admins[chat_id] = admins_


def gett(chat_id: Union[str, int]) -> Union[List[User], bool]:
    if isinstance(chat_id, int):
        chat_id = str(chat_id)

    if chat_id in admins:
        return admins[chat_id]

    return False
async def get_administrators(chat: Chat) -> List[User]:
    _get = gett(chat.id)

    if _get:
        return _get
    else:
        set(chat.id, [member.user for member in await chat.get_members(filter="administrators")])
        return await get_administrators(chat)

def errors(func: Callable) -> Coroutine:
    async def wrapper(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply(f"❗️ {type(e).__name__}: {e}")
    return wrapper


def admins_only(func: Callable) -> Coroutine:
    async def wrapper(client: Client, message: Message):
        if message.from_user.id in Adminsettings:
            return await func(client, message)
        admins = await get_administrators(message.chat)
        for admin in admins:
            if admin.id == message.from_user.id:
                return await func(client, message)
    return wrapper


@setbot.on_message(
    filters.command("pause")
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def pause(client: Client, message: Message):
    if vcbot is None:
      return
    vcbot.pause_stream(message.chat.id)
    await message.reply_text("⏸ Paused.")


@setbot.on_message(
    filters.command("resume")
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def resume(client: Client, message: Message):
    if vcbot is None:
      return
    vcbot.resume_stream(message.chat.id)
    await message.reply_text("▶️ Resumed.")


@setbot.on_message(
    filters.command(["stop", "end"])
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def stop(client: Client, message: Message):
    if vcbot is None:
      return
    try:
        clear(message.chat.id)
    except:
        pass

    vcbot.leave_group_call(message.chat.id)
    await message.reply_text("⏹ Stopped streaming.")


@setbot.on_message(
    filters.command(["skip", "next"])
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def skip(client: Client, message: Message):
    if vcbot is None:
      return
    chat_id = message.chat.id

    task_done(chat_id)
    await message.reply_text("Processing")
    if is_empty(chat_id):
        vcbot.leave_group_call(chat_id)
        await message.reply_text("nothing in queue")
    else:
        vcbot.change_stream(
            chat_id, sira.get(chat_id)["file_path"]
        )

        await message.reply_text("⏩ Skipped the current song.")


@setbot.on_message(
    filters.command("admincache")
)
@errors
@admins_only
async def admincache(client, message: Message):
    if vcbot is None:
      return
    set(message.chat.id, [member.user for member in await message.chat.get_members(filter="administrators")])
    await message.reply_text("❇️ Admin cache refreshed!")

#@setbot.on_inline_query()
#async def search(client: Client, query: InlineQuery):
#    answers = []
#    search_query = query.query.lower().strip().rstrip()

#    if search_query == "":
#       await client.answer_inline_query(
#            query.id,
#            results=answers,
#            switch_pm_text="Type a YouTube video name...",
#           switch_pm_parameter="help",
#           cache_time=0
#        )
#   else:
#        videosSearch = VideosSearch(search_query, limit=50)

#        for v in videosSearch.result()["result"]:
#            answers.append(
#                InlineQueryResultArticle(
 #                   title=v["title"],
  #                  description="{}, {} views.".format(
 #                       v["duration"],
 #                       v["viewCount"]["short"]
#                    ),
 #                   input_message_content=InputTextMessageContent(
#                        "https://www.youtube.com/watch?v={}".format(
 #                           v["id"]
 #                       )
 #                  ),
 #                   thumb_url=v["thumbnails"][0]["url"]
#                )
  #          )

  #      try:
 #           await query.answer(
 #               results=answers,
  #              cache_time=0
  #          )
  #      except errors.QueryIdInvalid:
  #          await query.answer(
     #           results=answers,
   #             cache_time=0,
 #               switch_pm_text="Error: Search timed out",
     #           switch_pm_parameter="",
     #       )
@setbot.on_message(
    filters.command("play")
    & filters.group
    & ~ filters.edited
)
@errors
async def play(client: Client, message_: Message):
    if vcbot is None:
      return
    audio = (message_.reply_to_message.audio or message_.reply_to_message.voice) if message_.reply_to_message else None
    chat_id=message_.chat.id
    res = await message_.reply_text("🔄 Processing...")

    if audio:
        if round(audio.duration / 60) > 10:
            raise DurationLimitError(
                f"Videos longer than 10 minute(s) aren't allowed, the provided video is {audio.duration / 60} minute(s)"
            )

        file_name = audio.file_id + audio.file_name.split(".")[-1]
        file_path = await convert(await message_.reply_to_message.download(file_name))
    else:
        messages = [message_]
        text = ""
        offset = None
        length = None

        if message_.reply_to_message:
            messages.append(message_.reply_to_message)

        for message in messages:
            if offset:
                break

            if message.entities:
                for entity in message.entities:
                    if entity.type == "url":
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break

        if offset == None:
            await res.edit_text("❕ You did not give me anything to play.")
            return

        url = text[offset:offset+length]

        file_path =await convert(download(url))

    if message_.chat.id in vcbot.active_calls:
        position = add(message_.chat.id, file_path)
        await res.edit_text(f"#️⃣ Queued at position {position}.")
    else:
        await res.edit_text("▶️ Playing...")
        res.delete
        m = await client.send_photo(
        chat_id=message_.chat.id,
        photo="https://telegra.ph/file/c6f15b74062eeb555d9b9.jpg",
        caption=f"Playing Your song Via king music bot.",
         ) 
        vcbot.join_group_call(message_.chat.id, file_path)
@vcbot.on_stream_end()
def on_stream_end(chat_id: int) -> None:
    task_done(chat_id)

    if is_empty(chat_id):
        vcbot.leave_group_call(chat_id)
    else:
        vcbot.change_stream(
            chat_id, sira.get(chat_id)["file_path"]
        )
