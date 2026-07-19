import aiohttp

session = aiohttp.ClientSession(
    headers={
        "User-Agent": "RonovaBot/1.0 (https://github.com/BreezeKun; contact: test@email.com)"
    }
)