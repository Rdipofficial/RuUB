from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.enums import ButtonStyle

from ..utilities import eval_helper
from config import ADMIN_ID


@Client.on_inline_query(filters.regex("googleit") & filters.user(ADMIN_ID))
async def inline_googleit(c: Client, q: InlineQuery):
    url = eval_helper.get("googleit_url", "https://letmegooglethat.com")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Open Google", url=url, style=ButtonStyle.PRIMARY)]
    ])

    await q.answer([
        InlineQueryResultArticle(
            title="I've googled it for you",
            description=url,
            input_message_content=InputTextMessageContent(
                f"I've googled it for you click on below link :)"
            ),
            reply_markup=keyboard
        )
    ], cache_time=0)