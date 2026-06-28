import aiohttp

from config import TAVILY_KEY


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
            title   = item.get("title", "")
            content = item.get("raw_content") or item.get("content") or ""
            text += f"[{i}] {title}\n{content[:500]}\n\n"
        return text

    async def fetch_answer(self, context: str = "") -> str:
        try:
            prompt = self.query
            if context:
                prompt = (
                    f"Context from web search:\n{context[:3000]}"
                    f"\n\nQuestion: {self.query}"
                    f"\nAnswer concisely using the context above."
                )

            payload = {
                "prompt": prompt,
                "network": True,  
                "stream": False,
                "system": {
                    "userId": "#/chat/1722576084617",
                    "withoutContext": not bool(context),
                },
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.binjie.fun/api/generateStream",
                    headers={"Content-Type": "application/json"},
                    json=payload,
                ) as response:
                    return await response.text()

        except Exception as e:
            return f"Error: {e}"