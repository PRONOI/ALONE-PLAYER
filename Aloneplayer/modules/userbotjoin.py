# AdityaPlayer (Telegram bot project )
# Copyright (C)  Aditya Halder

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


from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from AdityaPlayer.helpers.decorators import authorized_users_only, errors
from AdityaPlayer.services.callsmusic.callsmusic import client as USER
from AdityaPlayer.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>🤖 Ʌʈ Fɩɤsʈ Ʌɗɗ Ɱɘ ƛs Ʌɗɱɩɳ Øƒ Yøʋɤ Ƈɦɑʈ ❗️</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "AdityaPlayer"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "**🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️**")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Ʌɭɤɘɑɗƴ ɩɳ Yøʋɤ Ƈɦɑʈ ...</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🤖 Fɭøøɗ Eɤɤøɤ - Ɱɑɳʋɑɭɭƴ Ʌɗɗ Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ ʈø Yøʋɤ Ƈɦɑʈ øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</b>",
        )
        return
    await message.reply_text(
        "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑʈ ❗️</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>👉 Ʋsɘrɓøʈ Ƈøʋɭɗɳ'ʈ Lɘɑⱱɘ Yøʋr Ɠrøʋƥ ! Ɱɑƴ ɓɘ Fɭøøɗωɑɩʈs.\n\n👉 Ør Ɱɑɳɳʋɑɭɭƴ Ƙɩƈƙ Ɱɘ Frøɱ Yøʉr Ɠrøʋƥ.</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        await message.reply("**👉 Ʌssɩsʈɑɲʈ Lɘɑⱱɩɳʛ Ʌɭɭ Ƈɦɑʈs ...**")
        for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"👉 Ʌssɩsʈɑɲʈ Lɘɑⱱɩɳʛ ... Lɘfʈ: {left} Ƈɦɑʈs. Fɑɩɭɘɗ: {failed} Ƈɦɑʈs.")
            except:
                failed=failed+1
                await lol.edit(f"👉 Ʌssɩsʈɑɲʈ Lɘɑⱱɩɳʛ ... Lɘfʈ: {left} Ƈɦɑʈs. Fɑɩɭɘɗ: {failed} Ƈɦɑʈs.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"👉 Lɘfʈ {left} Ƈɦɑʈs. Fɑɩɭɘɗ {failed} Ƈɦɑʈs.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("**❗ Ɩs Ƭɦɩs Ƈɦɑʈ Eⱱɘɳ Łɩɳƙɘɗ ❓**")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>🤖 Ʌʈ Fɩɤsʈ Ʌɗɗ Ɱɘ ƛs Ʌɗɱɩɳ Øƒ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "AdityaPlayer"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "**🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️**")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Ʌɭɤɘɑɗƴ ɩɳ Yøʋɤ Ƈɦɑɳɳɘɭ ...</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🤖 Fɭøøɗ Eɤɤøɤ - Ɱɑɳʋɑɭɭƴ Ʌɗɗ Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ ʈø Yøʋɤ Ƈɦɑɳɳɘɭ øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ ...</b>",
        )
        return
    await message.reply_text(
        "<b>🤖 Ʌssɩsʈɑɳƈɘ Usɘɤɓøʈ Jøɩɳɘɗ Yøʋɤ Ƈɦɑɳɳɘɭ ❗️</b>",
    )
    

