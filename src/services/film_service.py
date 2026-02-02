import asyncio
from src.models.film import Film, FilmResponse, PlanetSummary
from src.services.swapi_client import SWAPIClient

class FilmService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def _extract_id(self, url: str) -> int:
        return int(url.rstrip('/').split('/')[-1])
    
    async def get_film_enriched(self, film_id: int) -> FilmResponse:
        raw_data = await self.swapi_client.get(f"/films/{film_id}/")
        film = Film(**raw_data)
        planet_data = await asyncio.gather(*[self.swapi_client.get(planet_url) for planet_url in film.planets])
        
        return FilmResponse(
            id = film_id,
            title = film.title,
            director = film.director,
            producer = film.producer,
            opening_crawl = film.opening_crawl,
            release_date = film.release_date,
            characters = {"total_characters": len(film.characters)},
            planets = [PlanetSummary(
                id = self._extract_id(planet['url']),
                name = planet['name'],
                climate = planet['climate'],
                terrain = planet['terrain']
            ) for planet in planet_data],
            statistics = {
                "total_characters": len(film.characters),
                "total_planets": len(planet_data),
                "total_species": len(film.species),
                "total_vehicles": len(film.vehicles),
                "total_starships": len(film.starships)
            }
        )
