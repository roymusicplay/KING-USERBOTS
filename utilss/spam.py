from pyrogram import filters
from pyrogram.types import Message
from kingbot import kingbot, setbot , vr , Adminsettings

@kingbot.on_message(filters.user(Adminsettings) & filters.command("spam", vr.get("HNDLR")))
async def spam(client, message):
    await message.delete()
    times = message.command[1]
    to_spam = " ".join(message.command[2:])
    if message.chat.type in ["supergroup", "group"]:
        for _ in range(int(times)):
            await client.send_message(
                message.chat.id, to_spam, reply_to_message_id=ReplyCheck(message)
            )
            await asyncio.sleep(0.20)

    if message.chat.type == "private":
        for _ in range(int(times)):
            await client.send_message(message.chat.id, to_spam)
            await asyncio.sleep(0.20)


@kingbot.on_message(filters.user(Adminsettings) & filters.command("spamstk", vr.get("HNDLR")))
async def spam_stick(client, message):
    if not message.reply_to_message:
        await message.edit_text("**reply to a sticker with amount you want to spam**")
        return
    if not message.reply_to_message.sticker:
        await message.edit_text(text="**reply to a sticker with amount you want to spam**")
        return
    else:
        times = message.command[1]
        if message.chat.type in ["supergroup", "group"]:
            for _ in range(int(times)):
                sticker=message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                    reply_to_message_id=ReplyCheck(message),
                )
                await asyncio.sleep(0.20)

        if message.chat.type == "private":
            for _ in range(int(times)):
                sticker=message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id, sticker
                )
                await asyncio.sleep(0.20)
