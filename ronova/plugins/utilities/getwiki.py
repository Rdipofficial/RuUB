import aiohttp

async def wiki_search(query: str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    headers = {
        "User-Agent": "MyTelegramBot/1.0 (https://example.com; your@email.com)"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None

            data = await resp.json()

            title = data.get("title", query)
            thumbnail = data.get("originalimage", {}).get("source", "")
            description = data.get("description", "")
            source_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            summary = data.get("extract", "")

            return title, thumbnail, description, source_url, summary