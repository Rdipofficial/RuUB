import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from ..filters import check
from..shared import PREMIUM_STATE
from config import ADMIN_ID


@Client.on_message(check() & filters.user(ADMIN_ID))
async def prem_click(c: Client, m: Message):

    if PREMIUM_STATE.status:
        button = m.reply_markup.inline_keyboard[0][0]

        await c.request_callback_answer(
            chat_id=m.chat.id,
            message_id=m.id,
            callback_data=button.callback_data
        )
    