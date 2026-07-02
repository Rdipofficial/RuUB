from pyrogram import Client, filters
from pyrogram.types import (InputRichMessage, InlineQuery,
                             InlineQueryResultArticle, InputRichMessageContent)

from ..utilities import wiki_search


def _escape(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")

    )

def fix_wiki_thumb(url: str, size: int = 330) -> str:
    if not url:
        return None

    if "upload.wikimedia.org" in url:
        import re
        return re.sub(r"\d+px", f"{size}px", url)

    return url


def build_rich_wiki_html(title, thumbnail, description, source_url, summary) -> str:
    title = _escape(title)
    description = _escape(description)
    summary = _escape(summary)
    thumbnail = _escape(thumbnail)

    parts = []

    if thumbnail:
        parts.append(f'<tg-slideshow><img src="{fix_wiki_thumb(thumbnail)}"/></tg-slideshow>')

    parts.append(f"<h1>{title}</h1>")
    parts.append("<hr/>")

    if summary:
        parts.append(
            "<details open>"
            "<summary><b>Summary</b></summary>"
            f"<blockquote>{summary}</blockquote>"
            "</details>"
        )
        parts.append("<hr/>")

    if description:
        parts.append(
            "<details>"
            "<summary><b>Description</b></summary>"
            f"<blockquote>{description}Wikipedia</blockquote>"
            "</details>"
        )
        parts.append("<hr/>")

    if source_url:
        link = _escape(source_url)
        parts.append(f'<p><a href="{link}">Read full article</a></p>')

    return "".join(parts)


def build_not_found_html(query: str) -> str:
    return (
        "<h2>Article not found</h2>"
        f"<p>No Wikipedia summary could be located for \u201c{_escape(query)}\u201d.</p>"
    )


@Client.on_inline_query(filters.regex(r"wiki (.+)"))
async def inline_wiki(c: Client, q: InlineQuery):
    name = q.matches[0].group(1)
    result = await wiki_search(name)

    rich_text = build_rich_wiki_html(*result) if result else build_not_found_html(name)

    await q.answer([
        InlineQueryResultArticle(
            title=f"Wiki: {name}",
            input_message_content=InputRichMessageContent(
                InputRichMessage(html=rich_text)
            )
        )
    ], cache_time=0)