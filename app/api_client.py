import aiohttp
from app.config import settings

async def fetch_disaster_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}", headers={"Authorization": f"Bearer {settings.API_KEY}"}) as response:
            return await response.json()
