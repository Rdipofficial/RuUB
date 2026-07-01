from pyrogram import Client, filters
from pyrogram.types import (InputRichMessage, InlineQuery,
                             InlineQueryResultArticle, InputRichMessageContent)

from ..utilities import get_full_movie


def _escape(text) -> str:
    if not text:
        return ""
    return (
        str(text).replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;")
    )


def build_movie_html(poster, banner, title, overview, genre, release, rating, runtime) -> str:
    title = _escape(title)
    release = _escape(release)

    clean_desc = _escape(
        (overview or "N/A")
        .replace("<br><br>\n", "\n\n")
        .replace("<br>", " ")
        .strip()
    )

    genre_list = "".join(f"<li>{_escape(g)}</li>" for g in genre) if genre else "<li>N/A</li>"

    images = "".join(f'<img src="{_escape(src)}"/>' for src in (banner, poster) if src)
    slideshow = f"<tg-slideshow>{images}</tg-slideshow>" if images else ""

    return f"""{slideshow}

<h1>{title}</h1>

<hr/>

<table bordered striped>
<tr><td><b>Release</b></td><td><code>{release}</code></td></tr>
<tr><td><b>Rating</b></td><td><code>{rating}/10</code></td></tr>
<tr><td><b>Runtime</b></td><td><code>{runtime} min</code></td></tr>
</table>

<hr/>

<details>
<summary><b>Genres</b></summary>
<ul>{genre_list}</ul>
</details>

<hr/>

<details open>
<summary><b>Synopsis</b></summary>
<blockquote>{clean_desc}</blockquote>
</details>"""


def build_not_found_html(query: str) -> str:
    return (
        "<h2>Movie not found</h2>"
        f"<p>No results for \u201c{_escape(query)}\u201d.</p>"
    )


@Client.on_inline_query(filters.regex(r"moviename (.+)"))
async def inline_movie(c: Client, q: InlineQuery):
    name = q.matches[0].group(1)
    result = await get_full_movie(name)

    rich_text = build_movie_html(*result) if result else build_not_found_html(name)

    await q.answer([
        InlineQueryResultArticle(
            title=f"Movie: {name}" if result else "Not found",
            input_message_content=InputRichMessageContent(
                InputRichMessage(html=rich_text)
            )
        )
    ], cache_time=0)