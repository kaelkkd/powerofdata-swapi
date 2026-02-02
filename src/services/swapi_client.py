import aiohttp
from datetime import datetime, timedelta
from urllib.parse import urljoin
from typing import Optional, Dict, Any, Tuple

class SWAPIClient:
    def __init__(self, cache_time_hours: int = 24):
        self.base_url = "https://swapi.dev/api"
        self.session: Optional[aiohttp.ClientSession] = None
        self._cache: Dict[str, Tuple[Dict[str, Any], datetime]] = {}
        self._cache_duration = timedelta(hours=cache_time_hours)
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session
    
    def _is_cache_valid(self, cached_time: datetime) -> bool:
        return datetime.now() - cached_time < self._cache_duration
    
    async def get(self, endpoint: str, params: Optional[dict] = None) -> Dict[str, Any]:
        if endpoint.startswith('http'):
            url = endpoint
        else:
            endpoint = endpoint.lstrip('/')
            url = urljoin(self.base_url + '/', endpoint)
        
        cache_key = url
        if params:
            cache_key = f"{url}?{'&'.join(f'{k}={v}' for k, v in sorted(params.items()))}"

        if cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if self._is_cache_valid(cached_time):
                return cached_data
            else:
                del self._cache[cache_key]
        
        session = await self._get_session()
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            
        self._cache[cache_key] = (data, datetime.now())

        return data
    
    def clear_cache(self):
        self._cache.clear()

    async def close(self):
        if self.session:
            await self.session.close()