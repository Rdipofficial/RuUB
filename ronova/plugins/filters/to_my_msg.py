from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatType, MessageEntityType

from .errors import NoUser


def to_me(uid: int | None = None):
    async def func(_, c: Client, m: Message):
        if uid == None:
            raise NoUser("please profide a user id to_me(uid:int = your_user_id)")
        if m.chat.type == ChatType.PRIVATE:
            return True

        if m.reply_to_message and m.reply_to_message.from_user:
            if m.reply_to_message.from_user.id == uid:
                return True
            
        if m.entities:
            for ent in m.entities:
                if ent.type == MessageEntityType.TEXT_MENTION:
                    if ent.user and ent.user.id == uid:
                        return True

                elif ent.type == MessageEntityType.MENTION:
                    me = await c.get_me()
                    if m.text and f"@{me.username}" in m.text:
                        return True

        return False

    return filters.create(func, name="ToMe")