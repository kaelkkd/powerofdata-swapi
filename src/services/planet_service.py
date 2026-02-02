import asyncio
from src.models.planet import Planet, PlanetResponse, PeopleSummary, FilmSummary
from src.services.swapi_client import SWAPIClient

class PlanetService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def _extract_id(self, url: str) -> int:
        return int(url.rstrip('/').split('/')[-1])

    async def get_planet_enriched(self, planet_id: int) -> PlanetResponse:
        raw_data = await self.swapi_client.get(f"/planets/{planet_id}/")
        planet = Planet(**raw_data)
        residents_data = await asyncio.gather(*[self.swapi_client.get(resident_url) for resident_url in planet.residents])
        films_data = await asyncio.gather(*[self.swapi_client.get(film_url) for film_url in planet.films])

        return PlanetResponse(
            id=planet_id,
            name=planet.name,
            diameter=planet.diameter,
            rotation_period=planet.rotation_period,
            orbital_period=planet.orbital_period,
            gravity=planet.gravity,
            population=planet.population,
            climate=planet.climate,
            terrain=planet.terrain,
            surface_water=planet.surface_water,
            residents=[
                PeopleSummary(
                    id=self._extract_id(resident['url']),
                    name=resident['name']
                ) for resident in residents_data
            ],
            films=[
                FilmSummary(
                    id=self._extract_id(film['url']),
                    title=film['title'],
                    episode_id=film['episode_id'],
                    release_date=film['release_date']
                ) for film in films_data
            ],
            statistics={
                "total_residents": len(residents_data),
                "total_films": len(films_data)
            }
        )