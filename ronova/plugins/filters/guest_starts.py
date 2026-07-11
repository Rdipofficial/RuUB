from pyrogram import Client, filters
from pyrogram.types import Message

def starts(prefix:str):
    async def func(flt, c:Client, m:Message):
        if not m.text:
            return False
        return m.text.startswith(prefix)
    return filters.create(func, name="StartsFilter")