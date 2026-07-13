import time
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType, MessageMediaType, MessageEntityType
from pyrogram.errors import FloodWait
from pyrogram.types import Message, ReplyParameters

from config import ADMIN_ID, PREFIXES
from ..shared import AFK_DATA
from ..utilities import format_time, refresh_data, send, extract_media
from ..filters import to_me

@Client.on_message(filters.command(["afk", "brb"], prefixes=PREFIXES) & filters.user(ADMIN_ID), group= 2)
async def afk(c:Client, m:Message):
    if AFK_DATA.status:
        duration = format_time(int(time.time() - AFK_DATA.afk_time))
        await send(c, m, f"{m.from_user.mention} is back after {duration}")
        refresh_data()
        return

    AFK_DATA.status = True
    AFK_DATA.afk_time = time.time()

    if len(m.command) > 1:
        AFK_DATA.reason = m.text.split(maxsplit=1)[1]

    if m.reply_to_message:
        AFK_DATA.file_id, AFK_DATA.file_type = extract_media(m.reply_to_message)

    text = f"{m.from_user.mention} is now AFK"
    if AFK_DATA.reason:
        text += f"\nReason: {AFK_DATA.reason}"

    await send(c, m, text)

@Client.on_message(filters.me, group= 1)
async def rem_afk(c:Client, m:Message):
    if AFK_DATA.status:
        duration = format_time(int(time.time() - AFK_DATA.afk_time))
        await send(c, m, f"{m.from_user.mention} is back after {duration}")
        refresh_data()
        return
    else:
        return

@Client.on_message(
    (filters.private | filters.mentioned | to_me(ADMIN_ID[0]))
    & ~filters.me
    & ~filters.command(["afk", "brb"], prefixes=PREFIXES),
    group=0
)
async def on_afk(c: Client, m: Message):

    if not AFK_DATA.status:
        return

    if not m.from_user:
        return

    if m.from_user.id in AFK_DATA.users:
        return

    AFK_DATA.users.append(m.from_user.id)

    duration = format_time(int(time.time() - AFK_DATA.afk_time))
    user = await c.get_users(ADMIN_ID[0])

    text = f"{user.mention} is AFK (since {duration})"

    if AFK_DATA.reason:
        text += f"\nReason: {AFK_DATA.reason}"

    await send(c, m, text)