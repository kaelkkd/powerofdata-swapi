import aiohttp
from urllib.parse import urljoin
from typing import Optional, Dict, Any

class SWAPIClient:
    def __init__(self):
        self.base_url = "https://swapi.dev/api"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session
    
    async def get(self, endpoint: str, params: Optional[dict] = None) -> Dict[str, Any]:
        session = await self._get_session()
        if endpoint.startswith('http'):
            url = endpoint
        else:
            endpoint = endpoint.lstrip('/')
            url = urljoin(self.base_url + '/', endpoint)
        
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            
            return await response.json()
    
    async def close(self):
        if self.session:
            await self.session.close()