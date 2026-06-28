import os

from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,CallbackQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle
from config import ADMIN_ID

@Client.on_inline_query(filters.regex("logs") & filters.user(ADMIN_ID))
async def inline_logs(c: Client, q: InlineQuery):

    if not os.path.exists("logs.txt"):
        text = "❌ Log file not found."
    else:
        with open("logs.txt", encoding="utf-8") as f:
            lines = f.readlines()

        tail = "".join(lines[-20:]).strip()

        if not tail:
            text = "📭 Log file is empty."
        else:
            text = f"<b>📋 Recent Logs</b>\n<pre>{tail[:4000]}</pre>"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑 Clear Logs", callback_data="clear_logs", style = ButtonStyle.DANGER)]
    ])

    await q.answer([
        InlineQueryResultArticle(
            title="📋 View Logs",
            input_message_content=InputTextMessageContent(
                text
            ),
            reply_markup=keyboard
        )
    ], cache_time=0)

@Client.on_callback_query(filters.regex("clear_logs"))
async def clear_logs_cb(c: Client, cb:CallbackQuery):

    from config import ADMIN_ID

    if cb.from_user.id not in ADMIN_ID:
        return await cb.answer("Not allowed", show_alert=True)

    import os

    if not os.path.exists("logs.txt"):
        return await cb.answer("Log file not found", show_alert=True)

    open("logs.txt", "w").close()

    await cb.answer("Logs cleared", show_alert=True)

    await c.edit_inline_text(
        inline_message_id=cb.inline_message_id,
        text="🧹 Logs have been cleared."
    )