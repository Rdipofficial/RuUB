from pyrogram import filters, Client
from pyrogram.types import Message


def nobot():
    async def func(flt, c: Client, m: Message):
        return bool(m.from_user and not m.from_user.is_bot)

    return filters.create(func, name="NoBotFilter")