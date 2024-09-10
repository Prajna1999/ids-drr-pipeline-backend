# flaskr/api_client.py

import aiohttp
from flaskr.config import settings
from flask import g


async def fetch_disaster_data():
    token = g.token
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}",
                               headers={"Authorization": f"Bearer {token}"}) as response:
            return await response.json()
