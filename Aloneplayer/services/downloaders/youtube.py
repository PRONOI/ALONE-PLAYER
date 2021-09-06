# Aditya Player - Telegram bot for streaming audio in group calls
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

# Modified by Inukaasith


from os import path

from youtube_dl import YoutubeDL

from AdityaPlayer.config import DURATION_LIMIT
from AdityaPlayer.helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"❌ **Vɩɗɘøs Løɳʛɘr ʈɦɑɳ {DURATION_LIMIT} ɱɩɳʉʈɘ(s) ɑrɘ Ɲøʈ Ʌɭɭøωɘɗ, Ƭɦɘ Ƥrøⱱɩɗɘɗ Vɩɗɘø ɩs {duration} ɱɩɳʉʈɘ(s)"
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"❌ **Vɩɗɘøs Løɳʛɘr ʈɦɑɳ {DURATION_LIMIT} ɱɩɳʉʈɘ(s) ɑrɘ Ɲøʈ Ʌɭɭøωɘɗ, Ƭɦɘ Ƥrøⱱɩɗɘɗ Vɩɗɘø ɩs {duration} ɱɩɳʉʈɘ(s)"
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
    
