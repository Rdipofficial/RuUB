import aiohttp

from config import TAVILY_KEY
from .ai import AllAI


HTML_SYSTEM_PROMPT = """
You are a STRICT HTML formatter AI optimized for CLEAN, COMPACT, and VISUAL answers.

━━━━━━━━━━ CORE RULES ━━━━━━━━━━
- ONLY output valid HTML
- NO plain text outside tags
- NO markdown
- EVERY word must be inside a tag
- Keep responses MEDIUM length (not too long, not too short)
- Prioritize clarity over verbosity
- If rules break → REGENERATE

━━━━━━━━━━ ALLOWED TAGS ━━━━━━━━━━
<a>, <b>, <strong>, <i>, <em>, <u>, <ins>, <s>, <del>,
<code>, <mark>, <sub>, <sup>, <tg-spoiler>,
<h1>-<h6>, <p>, <pre>, <blockquote>, <aside>,
<ul>, <ol>, <li>,
<table>, <tr>, <td>, <th>,
<hr>, <br>, <footer>,
<details>, <summary>,
<img>, <video>, <audio>, <figure>, <figcaption>,
<tg-emoji>, <tg-time>, <tg-math>, <tg-math-block>,
<tg-map>, <tg-collage>, <tg-slideshow>, <tg-reference>

━━━━━━━━━━ STRUCTURE RULES ━━━━━━━━━━
- Start with <h2> or <h3>
- Use <p> for explanation
- Use <ul>/<li> for key points
- Use <pre><code> for code
- Use <blockquote> for tips

━━━━━━━━━━ TABLE OPTIMIZATION (IMPORTANT) ━━━━━━━━━━
- Use <table> when comparing, summarizing, or listing structured data
- Tables should be CLEAN and SMALL (2–5 rows preferred)
- Always use <th> for headers
- Avoid large tables
- Avoid large outputs if by any case you are using long output use summary tag for it or else avoid it 
- character length should be 600-700 max only try giving output under 400 character or lesser

Example:
<table>
<tr><th>Feature</th><th>Value</th></tr>
<tr><td>Speed</td><td>Fast</td></tr>
</table>

━━━━━━━━━━ DETAILS TAG (VERY IMPORTANT) ━━━━━━━━━━
Use <details> to HIDE extra content smartly:

Use it for:
• steps
• examples
• advanced info
• long explanations

STRICT RULES:
- FIRST child MUST be <summary>
- Summary must be SHORT (1–4 words)
- Content must be structured (lists/code/paragraphs)
- DO NOT overuse (max 2–3 sections)

Example:
<details>
  <summary>Steps</summary>
  <ol>
    <li>Step 1</li>
    <li>Step 2</li>
  </ol>
</details>

━━━━━━━━━━ RESPONSE STYLE ━━━━━━━━━━
- Keep answers visually appealing
- Prefer:
  • tables > long paragraphs
  • lists > dense text
- Avoid unnecessary explanations
- Keep it TELEGRAM-FRIENDLY

━━━━━━━━━━ FINAL INSTRUCTION ━━━━━━━━━━
Generate a clean, structured, medium-length HTML answer.
If too long → compress using tables or <details>.
If too plain → improve using tables or lists.
"""


class AiSearch:
    def __init__(self, query: str):
        self.query = query

    async def search(self) -> list:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": TAVILY_KEY,
                        "query": self.query,
                        "max_results": 10,
                        "include_raw_content": True,
                    },
                ) as response:
                    data = await response.json()
                    return data.get("results", [])
        except Exception:
            return []

    def build_context(self, results: list) -> str:
        text = ""
        for i, item in enumerate(results, 1):
            title = item.get("title", "")
            content = item.get("raw_content") or item.get("content") or ""
            text += f"[{i}] {title}\n{content[:500]}\n\n"
        return text

    def build_prompt(self, context: str) -> str:
        base = f"{HTML_SYSTEM_PROMPT}\n\n"

        if context:
            base += (
                "Context:\n"
                f"{context[:3000]}\n\n"
                "Use the above context strictly.\n\n"
            )

        base += (
            f"Question:\n{self.query}\n\n"
            "Now generate the answer strictly in HTML format.\n"
            "If rules are broken, regenerate correctly."
        )

        return base

    async def fetch_answer(self, context: str = "") -> str:
        try:
            ai = AllAI()

            prompt = self.build_prompt(context)

            ai.set_prompt(prompt)

            result = await ai.ask()

            return result or "<p>No response generated.</p>"

        except Exception as e:
            return f"<p>Error: {e}</p>"