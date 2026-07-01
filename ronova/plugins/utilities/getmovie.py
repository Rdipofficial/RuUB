import aiohttp

from config import TMDB_KEY

API_KEY = TMDB_KEY
BASE_URL = "https://api.themoviedb.org/3"

_session: aiohttp.ClientSession | None = None


async def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


async def get_full_movie(query: str):
    try:
        session = await get_session()

        async with session.get(
            f"{BASE_URL}/search/movie",
            params={"api_key": API_KEY, "query": query},
            timeout=aiohttp.ClientTimeout(total=4)
        ) as search:
            search_data = await search.json()

        if not search_data.get("results"):
            return None

        movie = search_data["results"][0]

        async with session.get(
            f"{BASE_URL}/movie/{movie['id']}",
            params={"api_key": API_KEY},
            timeout=aiohttp.ClientTimeout(total=4)
        ) as details:
            data = await details.json()

        poster_path = data.get("poster_path")
        backdrop_path = data.get("backdrop_path")

        poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
        banner = f"https://image.tmdb.org/t/p/w780{backdrop_path}" if backdrop_path else ""

        title = data.get("title", "N/A")
        overview = data.get("overview", "No description available.")
        genres = [g["name"] for g in data.get("genres", [])]

        release = data.get("release_date", "N/A")
        rating = data.get("vote_average", 0)
        runtime = data.get("runtime", 0)

        return (poster, banner, title, overview, genres, release, rating, runtime)

    except Exception as e:
        print("TMDB Error:", e)
        return None