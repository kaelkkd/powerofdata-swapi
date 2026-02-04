import asyncio
from src.models.people import People, PeopleResponse, PeopleListResponse, PeopleListItem, PlanetSummary, FilmSummary
from src.services.swapi_client import SWAPIClient

class PeopleService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def _extract_id(self, url: str) -> int:
        return int(url.rstrip('/').split('/')[-1])

    async def get_people_enriched(self, people_id: int) -> PeopleResponse:
        raw_data = await self.swapi_client.get(f"/people/{people_id}/")
        people = People(**raw_data)
        homeworld_data = await self.swapi_client.get(people.homeworld)
        films_data = await asyncio.gather(*[self.swapi_client.get(film_url) for film_url in people.films])

        return PeopleResponse(
            id = people_id, 
            name = people.name,
            height = people.height,
            mass = people.mass,
            appearance = {
                "hair_color": people.hair_color,
                "skin_color": people.skin_color,
                "eye_color": people.eye_color
            },
            birth_year = people.birth_year,
            gender = people.gender,
            homeworld = PlanetSummary(
                id = self._extract_id(homeworld_data['url']),
                name = homeworld_data['name'],
                climate = homeworld_data['climate'],
                terrain = homeworld_data['terrain']
            ),
            films = [
                FilmSummary(
                    id = self._extract_id(film['url']),
                    title = film['title'],
                    episode_id = film['episode_id'],
                    release_date = film['release_date']
                ) for film in films_data
            ],
            statistics = {
                "total_films": len(films_data),
                "total_starships": len(people.starships),
                "total_vehicles": len(people.vehicles)
            }
        )

    async def get_people_list(self, page: int = 1) -> PeopleListResponse:
        raw_data = await self.swapi_client.get("/people/", params={"page": page})
        results = []

        for person_data in raw_data['results']:
            person = People(**person_data)
            homeworld_id = self._extract_id(person.homeworld)
            results.append(PeopleListItem(
                id=self._extract_id(person.url),
                name=person.name,
                gender=person.gender,
                birth_year=person.birth_year,
                homeworld_id=homeworld_id,
                height=person.height,
                mass=person.mass
            ))
        
        return PeopleListResponse(
            count=raw_data['count'],
            next=raw_data.get('next'),
            previous=raw_data.get('previous'),
            results=results
        )
