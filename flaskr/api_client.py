# flaskr/api_client.py

import aiohttp
from flaskr.config import settings
from flask import g
from urllib.parse import urljoin


async def fetch_disaster_data():
    token = g.token
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}",
                               headers={"Authorization": f"Bearer {token}"}) as response:
            return await response.json()


async def fetch_consolidated_flood_data(from_date, to_date):
    token = g.token
    base_url = "https://drims.veldev.com/api"
    endpoint = f"/reports/flood/getStateCumulativeData"

    params = {
        "fromDate": from_date,
        "toDate": to_date
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session:
        url = urljoin(base_url, endpoint)
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": f"Request failed with status {response.status}"}
