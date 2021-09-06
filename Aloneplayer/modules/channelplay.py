# AdityaPlayer (Telegram bot project)
# Copyright (C) 2021  AdityaHalder
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Voice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from AdityaPlayer.modules.play import generate_cover
from AdityaPlayer.modules.play import arq
from AdityaPlayer.modules.play import cb_admin_check
from AdityaPlayer.modules.play import transcode
from AdityaPlayer.modules.play import convert_seconds
from AdityaPlayer.modules.play import time_to_seconds
from AdityaPlayer.modules.play import changeImageSize
from AdityaPlayer.config import BOT_NAME as bn
from AdityaPlayer.config import DURATION_LIMIT
from AdityaPlayer.config import UPDATES_CHANNEL as updateschannel
from AdityaPlayer.config import que
from AdityaPlayer.function.admins import admins as a
from AdityaPlayer.helpers.errors import DurationLimitError
from AdityaPlayer.helpers.decorators import errors
from AdityaPlayer.helpers.admins import get_administrators
from AdityaPlayer.helpers.channelmusic import get_chat_id
from AdityaPlayer.helpers.decorators import authorized_users_only
from AdityaPlayer.helpers.filters import command, other_filters
from AdityaPlayer.helpers.gets import get_file_name
from AdityaPlayer.services.callsmusic import callsmusic
from AdityaPlayer.services.callsmusic.callsmusic import client as USER
from AdityaPlayer.services.converter.converter import convert
from AdityaPlayer.services.downloaders import youtube
from AdityaPlayer.services.queues import queues

chat_id = None



@Client.on_message(filters.command(["channelplaylist","cplaylist"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
    except:
      message.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return
    global que
    queue = que.get(lol)
    if not queue:
        await message.reply_text("**⭕️ Ƥɭɑƴɘɤ ɩs Ɩɗɭɘ ...**")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**▶️ Ɲøω Ƥɭɑƴɩɳʛ ɩɳ** {}".format(lel.linked_chat.title)
    msg += "\n♨️ " + now_playing
    msg += "\n💢 **Ʀɘʠʋɘʂʈɘɗ Ɓƴ** " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Qʋɘʋɘ**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n♨️ {name}"
            msg += f"\n💢 **Ʀɘʠʋɘʂʈɘɗ Ɓƴ** {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "**Sɘʈʈɩɳʛʂ Øƒ** **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "**Vøɭʋɱɘ :** {}%\n".format(vol)
            stats += "**Søɳʛʂ ɩɳ Qʋɘʋɘ :** `{}`\n".format(len(que))
            stats += "**Ɲøω Ƥɭɑƴɩɳʛ :** {}**\n".format(queue[0][0])
            stats += "**Ʀɘʠʋɘʂʈɘɗ Ɓƴ :** {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "cleave"),
                InlineKeyboardButton("⏸", "cpuse"),
                InlineKeyboardButton("▶️", "cresume"),
                InlineKeyboardButton("⏭", "cskip"),
            ],
            [
                InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", "cplaylist"),
            ],
            
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
                
            [InlineKeyboardButton("❌ Ƈɭøsɘ ❌", "ccls")],
        ]
    )
    return mar


@Client.on_message(filters.command(["channelcurrent","ccurrent"]) & filters.group & ~filters.edited)
async def ee(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("**🤖 Ɲø Vøɩƈɘ Ƈɦɑʈ Ɩɳsʈɑɳƈɘs Ʀʋŋɳɩɲʛ ɩɳ Ƭɦɩs Ƈɦɑʈ ...**")


@Client.on_message(filters.command(["channelplayer","cplayer"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("**🤖 Ɲø Vøɩƈɘ Ƈɦɑʈ Ɩɳsʈɑɳƈɘs Ʀʋŋɳɩɲʛ ɩɳ Ƭɦɩs Ƈɦɑʈ ...**")


@Client.on_callback_query(filters.regex(pattern=r"^(cplaylist)$"))
async def p_cb(b, cb):
    global que
    try:
      lel = await client.get_chat(cb.message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      return    
    que.get(lol)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(lol)
        if not queue:
            await cb.message.edit("**⭕️ Ƥɭɑƴɘɤ ɩs Ɩɗɭɘ ...**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**▶️ Ɲøω Ƥɭɑƴɩɳʛ ɩɳ** {}".format(conv.title)
        msg += "\n♨️ " + now_playing
        msg += "\n💢 **Ʀɘʠʋɘʂʈɘɗ Ɓƴ** " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Qʋɘʋɘ**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n♨️ {name}"
                msg += f"\n💢 **Ʀɘʠʋɘʂʈɘɗ Ɓƴ** {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(cplay|cpause|cskip|cleave|cpuse|cresume|cmenu|ccls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
      try:
        lel = await b.get_chat(cb.message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
        chet_id = lol
      except:
        return
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat
    

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "cpause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("❎ Ƈɦɑʈ ɩs Ɲøʈ Ƈøɳɳɘƈʈɘɗ ❗️", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("▶ ️Sʋƈƈɘssƒʋɭɭƴ Ƥɑʋsɘɗ ❗")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "cplay":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("❎ Ƈɦɑʈ ɩs Ɲøʈ Ƈøɳɳɘƈʈɘɗ ❗️", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("⏸ ️Sʋƈƈɘssƒʋɭɭƴ Ʀɘsʋɱɘɗ ❗")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "cplaylist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("**⭕️ Ƥɭɑƴɘɤ ɩs Ɩɗɭɘ ...**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "****▶️ Ɲøω Ƥɭɑƴɩɳʛ ɩɳ** {}".format(cb.message.chat.title)
        msg += "\n♨️ " + now_playing
        msg += "\n💢 **Ʀɘʠʋɘʂʈɘɗ Ɓƴ** " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Qʋɘʋɘ**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n♨️ {name}"
                msg += f"\n💢 **Ʀɘʠʋɘʂʈɘɗ Ɓƴ** {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "cresume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("❎ Ƈɦɑʈ ɩs Ɲøʈ Ƈøɳɳɘƈʈɘɗ øɤ Ʌɭɤɘɑɗƴ Ƥɭɑƴɩɳʛ ❗️", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("⏸ ️Sʋƈƈɘssƒʋɭɭƴ Ʀɘsʋɱɘɗ ❗")
    elif type_ == "cpuse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("❎ Ƈɦɑʈ ɩs Ɲøʈ Ƈøɳɳɘƈʈɘɗ øɤ Ʌɭɤɘɑɗƴ Ƥɑʋsɘɗ ❗️", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("▶ ️Sʋƈƈɘssƒʋɭɭƴ Ƥɑʋsɘɗ ❗")
    elif type_ == "ccls":
        await cb.answer("❎ Sʋƈƈɘssƒʋɭɭƴ Ƈɭøsɘɗ Ɱɘɳʋ ❎")
        await cb.message.delete()

    elif type_ == "cmenu":
        stats = updated_stats(conv, qeue)
        await cb.answer("✅ Sʋƈƈɘssƒʋɭɭƴ Øƥɘɳɘɗ Ɱɘɳʋ ✅")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "cleave"),
                    InlineKeyboardButton("⏸", "cpuse"),
                    InlineKeyboardButton("▶️", "cresume"),
                    InlineKeyboardButton("⏭", "cskip"),
                ],
                [
                    InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", "cplaylist"),
                ],
                
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
                
                [InlineKeyboardButton("❌ Ƈɭøsɘ ❌", "ccls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "cskip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("❎ Ƈɦɑʈ ɩs Ɲøʈ Ƈøɳɳɘƈʈɘɗ ❗️", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("**📵 Ɲø Ɱøɤɘ Ƥɭɑƴɭɩsʈ ...**\n**📱 Łɘɑⱱɩɳʛ Vøɩƈɘ Ƈɦɑʈ ...**")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("✅ Sʋƈƈɘssƒʋɭɭƴ Sƙɩƥƥɘɗ ❗️")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"**⏩ Sƙɩƥƥɘɗ Ƭɦɘ Søɳʛ ...**\n**▶️ Ɲøω Ƥɭɑƴɩɳʛ** **{qeue[0][0]}**"
                )

    else:
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("**✅ Sʋƈƈɘssƒʋɭɭƴ Łɘɑⱱɘɗ Ƭɦɘ Vøɩƈɘ Ƈɦɑʈ ✅**")
        else:
            await cb.answer("❎ Ƈɦɑʈ ɩs Ɲøʈ Ƈøɳɳɘƈʈɘɗ ❗️", show_alert=True)


@Client.on_message(filters.command(["channelplay","cplay"])  & filters.group & ~filters.edited)
@authorized_users_only
async def play(_, message: Message):
    global que
    lel = await message.reply("**🔄 Ƥɤøƈƈɘssɩɳʛ ...**")

    try:
      conchat = await _.get_chat(message.chat.id)
      conv = conchat.linked_chat
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("**❗️ Ʌɱ Ɩ Ʌɗɱɩɳ Øƒ Ƈɦɑɳɳɘɭ ❓**")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "Aditya Player"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>🤖 Ʀɘɱɘɱɓɘɤ ʈø Ʌɗɗ Ʌssɩsʈɑɳƈɘ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )
                    pass

                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🤖 Ʌʈ Fɩɤsʈ Ʌɗɗ Ɱɘ ƛs Ʌɗɱɩɳ Øƒ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🤖 Fɭøøɗ Eɤɤøɤ - Ɱɑɳʋɑɭɭƴ Ʌɗɗ Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</b>",
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Ɲøʈ ɩɳ Yøʋɤ Ƈɦɑɳɳɘɭ ...\nƤɭɘasɘ Ʌɗɗ ɩʈ  Ɱɑɳɳʋɑɭɭƴ Øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</i>"
        )
        return
    message.from_user.id
    text_links = None
    message.from_user.first_name
    await lel.edit("**🔎 Sɘɑɤƈɦɩɳʛ ...**")
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**❌ Vɩɗɘøs Łøɳʛɘɤ Ƭɦɑɳ {DURATION_LIMIT} Ɱɩɳʋʈɘ(s) Ʌɤɘ Ɲøʈ Ʌɭɭøωɘɗ ʈø Ƥɭɑƴ ❗"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", callback_data="cplaylist"),
                    InlineKeyboardButton("🎧 Ɱɘɳʋ 🎧", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
                [InlineKeyboardButton(text="❌ Ƈɭøsɘ ❌", callback_data="ccls")],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/793b7adbe8f4ca26bd7d9.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Łøƈɑɭɭƴ Ʌɗɗɘɗ"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("**🔄 Ƥɤøƈƈɘssɩɳʛ ...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "**🎶 Søɳʛ Ɲøʈ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Søɳʛ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**"
            )
            print(str(e))
            return
        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", callback_data="cplaylist"),
                    InlineKeyboardButton("🎧 Ɱɘɳʋ 🎧", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
                [InlineKeyboardButton(text="❌ Ƈɭøsɘ ❌", callback_data="ccls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("**🔄 Ƥɤøƈƈɘssɩɳʛ ...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "🎶 Søɳʛ Ɲøʈ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Søɳʛ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**"
            )
            print(str(e))
            return

        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", callback_data="cplaylist"),
                    InlineKeyboardButton("🎧 Ɱɘɳʋ 🎧", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
                [InlineKeyboardButton(text="❌ Ƈɭøsɘ ❌", callback_data="ccls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))
    chat_id = chid
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"**#⃣ Yøʋɤ Ʀɘʠʋɘsʈɘɗ Søɳʛ Qʋɘʋɘɗ ƛʈ Ƥøsɩʈɩøɳ** **{position}** ❗️",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = chid
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**▶️ Ƥɭɑƴɩɳʛ Ƭɦɘ Søɳʛ Ʀɘʠʋɘsʈɘɗ Ɓƴ {} ɩɳ Łɩɳƙɘɗ Ƈɦɑɳɳɘɭ ...**".format(
                message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()


@Client.on_message(filters.command(["channeldplay","cdplay"]) & filters.group & ~filters.edited)
@authorized_users_only
async def deezer(client: Client, message_: Message):
    global que
    lel = await message_.reply("**🔄 Ƥɤøƈƈɘssɩɳʛ ...**")

    try:
      conchat = await client.get_chat(message_.chat.id)
      conid = conchat.linked_chat.id
      conv = conchat.linked_chat
      chid = conid
    except:
      await message_.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("**❗️ Ʌɱ Ɩ Ʌɗɱɩɳ Øƒ Ƈɦɑɳɳɘɭ ❓**") 
    try:
        user = await USER.get_me()
    except:
        user.first_name = "AdityaPlayer"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await client.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message_.from_user.id:
                if message_.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>🤖 Ʀɘɱɘɱɓɘɤ ʈø Ʌɗɗ Ʌssɩsʈɑɳƈɘ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )
                    pass
                try:
                    invitelink = await client.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🤖 Ʌʈ Fɩɤsʈ Ʌɗɗ Ɱɘ ƛs Ʌɗɱɩɳ Øƒ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🤖 Fɭøøɗ Eɤɤøɤ - Ɱɑɳʋɑɭɭƴ Ʌɗɗ Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Ɲøʈ ɩɳ Yøʋɤ Ƈɦɑɳɳɘɭ ...\nƤɭɘasɘ Ʌɗɗ ɩʈ  Ɱɑɳɳʋɑɭɭƴ Øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</i>"
        )
        return
    requested_by = message_.from_user.first_name

    text = message_.text.split(" ", 1)
    queryy = text[1]
    query=queryy
    res = lel
    await res.edit(f"**🔎 Sɘɑɤƈɦɩɳʛ ...**")
    try:
        songs = await arq.deezer(query,1)
        if not songs.ok:
            await message_.reply_text(songs.result)
            return
        title = songs.result[0].title
        url = songs.result[0].url
        artist = songs.result[0].artist
        duration = songs.result[0].duration
        thumbnail = songs.result[0].thumbnail
    except:
        await res.edit("**🎶 Søɳʛ Ɲøʈ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Søɳʛ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**")
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", callback_data="cplaylist"),
                InlineKeyboardButton("🎧 Ɱɘɳʋ 🎧", callback_data="cmenu"),
            ],
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
            
            [InlineKeyboardButton(text="❌ Ƈɭøsɘ ❌", callback_data="ccls")],
        ]
    )
    file_path = await convert(wget.download(url))
    await res.edit("**🌁 Ɠɘɳɘɤɑʈɩɳʛ Ƭɦʋɱɓɳɑɩɭ ...**")
    await generate_cover(requested_by, title, artist, duration, thumbnail)
    chat_id = chid
    if chat_id in callsmusic.pytgcalls.active_calls:
        await res.edit("**✏️ Ʌɗɗɩɳʛ ɩɳ Qʋɘʋɘ ...**")
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.edit_text(f"**#⃣ Yøʋɤ Ʀɘʠʋɘsʈɘɗ Søɳʛ Qʋɘʋɘɗ ƛʈ Ƥøsɩʈɩøɳ** **{position}** ❗️")
    else:
        await res.edit_text(f"**▶️ Ƥɭɑƴɩɳʛ ...**")

        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)

    await res.delete()

    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"**▶️ Ƥɭɑƴɩɳʛ Ƭɦɘ Søɳʛ Vɩɑ Ɗɘɘzɘɤ ɩɳ Łɩɳƙɘɗ Ƈɦɑɳɳɘɭ ...**",
    )
    os.remove("final.png")


@Client.on_message(filters.command(["channelsplay","csplay"]) & filters.group & ~filters.edited)
@authorized_users_only
async def jiosaavn(client: Client, message_: Message):
    global que
    lel = await message_.reply("🔄 **Processing**")
    try:
      conchat = await client.get_chat(message_.chat.id)
      conid = conchat.linked_chat.id
      conv = conchat.linked_chat
      chid = conid
    except:
      await message_.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("**❗️ Ʌɱ Ɩ Ʌɗɱɩɳ Øƒ Ƈɦɑɳɳɘɭ ❓**")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "AdityaPlayer"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await client.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message_.from_user.id:
                if message_.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>🤖 Ʀɘɱɘɱɓɘɤ ʈø Ʌɗɗ Ʌssɩsʈɑɳƈɘ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )
                    pass
                try:
                    invitelink = await client.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🤖 Ʌʈ Fɩɤsʈ Ʌɗɗ Ɱɘ ƛs Ʌɗɱɩɳ Øƒ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🤖 Fɭøøɗ Eɤɤøɤ - Ɱɑɳʋɑɭɭƴ Ʌɗɗ Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            "<i> 🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Ɲøʈ ɩɳ Yøʋɤ Ƈɦɑɳɳɘɭ ...\nƤɭɘasɘ Ʌɗɗ ɩʈ  Ɱɑɳɳʋɑɭɭƴ Øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</i>"
        )
        return
    requested_by = message_.from_user.first_name
    chat_id = message_.chat.id
    text = message_.text.split(" ", 1)
    query = text[1]
    res = lel
    await res.edit(f"**🔎 Sɘɑɤƈɦɩɳʛ ...**")
    try:
        songs = await arq.saavn(query)
        if not songs.ok:
            await message_.reply_text(songs.result)
            return
        sname = songs.result[0].song
        slink = songs.result[0].media_url
        ssingers = songs.result[0].singers
        sthumb = "https://telegra.ph/file/f6086f8909fbfeb0844f2.png"
        sduration = int(songs.result[0].duration)
    except Exception as e:
        await res.edit("**🎶 Søɳʛ Ɲøʈ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Søɳʛ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**")
        print(str(e))
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📝 Ƥɭɑƴɭɩsʈ 📝", callback_data="cplaylist"),
                InlineKeyboardButton("🎧 Ɱɘɳʋ 🎧", callback_data="cmenu"),
            ],
                [
                    InlineKeyboardButton(text="🌐 Ƈɦɑɳɳɘɭ 🌐", url=f"{https://t.me/adityaserver}"),
                    InlineKeyboardButton(text="💬 Ɠɤøʋƥ 💬", url=f"{https://t.me/adityadiscus}"),
                ],
            [InlineKeyboardButton(text="❌ Ƈɭøsɘ ❌", callback_data="ccls")],
        ]
    )
    file_path = await convert(wget.download(slink))
    chat_id = chid
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = sname
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.delete()
        m = await client.send_photo(
            chat_id=message_.chat.id,
            reply_markup=keyboard,
            photo="final.png",
            caption=f"**#⃣ Yøʋɤ Ʀɘʠʋɘsʈɘɗ Søɳʛ Qʋɘʋɘɗ ƛʈ Ƥøsɩʈɩøɳ** **{position}** ❗️",
        )

    else:
        await res.edit_text(f"**▶️ Ƥɭɑƴɩɳʛ ...**")
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = sname
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
    await res.edit("**🌁 Ɠɘɳɘɤɑʈɩɳʛ Ƭɦʋɱɓɳɑɩɭ ...**")
    await generate_cover(requested_by, sname, ssingers, sduration, sthumb)
    await res.delete()
    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"**▶️ Ƥɭɑƴɩɳʛ Ƭɦɘ Søɳʛ Vɩɑ Sɑɑⱱɳ ɩɳ Łɩɳƙɘɗ Ƈɦɑɳɳɘɭ ...**",
    )
    os.remove("final.png")


# Author ~ Aditya Halder

