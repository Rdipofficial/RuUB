from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMIN_ID,PREFIXES

from ..utilities import AiSearch

@Client.on_message(filters.command("think", prefixes=PREFIXES) & filters.user(ADMIN_ID))
async def think(c:Client, m:Message):
    args = m.command[1:]

    if not args:
        return await m.reply(
            "**think Usage**\n\n"
            "`think <question>` — AI only\n"
            "`think adv <question>` — Web search + AI"
        )

    if args[0].lower() == "adv":
        query = " ".join(args[1:])
        if not query:
            return await m.reply("Usage: `think adv <question>`")

        msg = await m.reply("wait...")
        ai  = AiSearch(query)

        results = await ai.search()
        if not results:
            return await msg.edit("No results found.")

        # await msg.edit("Thinking...")
        context = ai.build_context(results)
        answer  = await ai.fetch_answer(context)

        sources = "\n".join(
            f"[{i}] {r.get('url', '')}" for i, r in enumerate(results[:5], 1)
        )
        await msg.delete()

        await m.reply(
            f"**🌐 Deep Think Result**\n\n"
            f"**Query:** {query}\n\n"
            f"**Answer:**\n{answer}\n\n"
            f"```Sources:\n{sources}```"
        )

    else:
        query  = " ".join(args)
        msg    = await m.reply("Thinking...")
        ai     = AiSearch(query)
        answer = await ai.fetch_answer()

        await msg.delete()

        await msg.edit(
            f"💭 **Think**\n\n"
            f"**Query:** `{query}`\n\n"
            f"{answer}"
        )