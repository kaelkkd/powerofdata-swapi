import asyncio
from src.models.starship import Starship, StarshipResponse, StarshipListResponse, StarshipListItem, PeopleSummary, FilmSummary
from src.services.swapi_client import SWAPIClient

class StarshipService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def _extract_id(self, url: str) -> int:
        return int(url.rstrip('/').split('/')[-1])

    async def get_starship_enriched(self, starship_id: int) -> StarshipResponse:
        raw_data = await self.swapi_client.get(f"/starships/{starship_id}/")
        starship = Starship(**raw_data)
        pilots_data = await asyncio.gather(*[self.swapi_client.get(pilot_url) for pilot_url in starship.pilots])
        films_data = await asyncio.gather(*[self.swapi_client.get(film_url) for film_url in starship.films])

        return StarshipResponse(
            id=starship_id,
            name=starship.name,
            model=starship.model,
            starship_class=starship.starship_class,
            manufacturer=starship.manufacturer,
            cost_in_credits=starship.cost_in_credits,
            length=starship.length,
            crew=starship.crew,
            passengers=starship.passengers,
            max_atmosphering_speed=starship.max_atmosphering_speed,
            hyperdrive_rating=starship.hyperdrive_rating,
            MGLT=starship.MGLT,
            cargo_capacity=starship.cargo_capacity,
            consumables=starship.consumables,
            pilots=[
                PeopleSummary(
                    id=self._extract_id(pilot['url']),
                    name=pilot['name'],
                    specie=pilot['specie']
                ) for pilot in pilots_data
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
                "total_pilots": len(pilots_data),
                "total_films": len(films_data)
            }
        )

    async def get_starships_list(self, page: int = 1) -> StarshipListResponse:
        raw_data = await self.swapi_client.get("/starships/", params={"page": page})
        results = []

        for starship_data in raw_data['results']:
            starship = Starship(**starship_data)
            results.append(StarshipListItem(
                id=self._extract_id(starship.url),
                name=starship.name,
                model=starship.model,
                starship_class=starship.starship_class,
                manufacturer=starship.manufacturer
            ))
        
        return StarshipListResponse(
            count=raw_data['count'],
            next=raw_data.get('next'),
            previous=raw_data.get('previous'),
            results=results
        )