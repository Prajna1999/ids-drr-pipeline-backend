# flaskr/api_client.py

import aiohttp
from flask import g
from urllib.parse import urljoin


async def fetch_consolidated_flood_data(from_date, to_date):
    token = g.token
    base_url = "https://drims.veldev.com"  # Make sure this is the correct base URL
    endpoint = "/reports/flood/getStateCumulativeData"

    params = {
        "fromDate": from_date,
        "toDate": to_date
    }

    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        url = urljoin(base_url, endpoint)
        async with session.get(url, params=params, headers=headers) as response:
            content_type = response.headers.get('Content-Type', '')

            if response.status == 200:
                if 'application/json' in content_type:
                    return await response.json()
                elif 'text/html' in content_type:
                    # If it's HTML, return the text content for debugging
                    text_content = await response.text()
                    # First 200 characters for brevity
                    return {"error": "Received HTML instead of JSON", "content": text_content[:200]}
                else:
                    return {"error": f"Unexpected content type: {content_type}"}
            else:
                # Handle error cases
                return {"error": f"Request failed with status {response.status}", "content": await response.text()}
