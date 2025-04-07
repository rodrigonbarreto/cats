import httpx
from typing import List, Dict, Any


async def get_external_dogs(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch dogs from external The Dog API

    Returns:
        List of dogs with information like id, url, width and height
    """
    url = f"https://api.thedogapi.com/v1/images/search?limit={limit}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        return response.json()
