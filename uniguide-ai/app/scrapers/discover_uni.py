import httpx

DISCOVER_UNI_URL = "https://discoveruni.gov.uk/api/courses"  # example; adjust to real

async def fetch_courses(limit: int = 50):
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(DISCOVER_UNI_URL, params={"limit": limit})
        resp.raise_for_status()
        data = resp.json()
        return data