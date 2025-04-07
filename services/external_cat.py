import httpx
from typing import List, Dict, Any


async def get_external_cats(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch cats from external TheCatAPI

    Returns:
        List of cats with information like id, url, width and height
    """
    url = f"https://api.thecatapi.com/v1/images/search?limit={limit}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        return response.json()
