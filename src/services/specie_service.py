import asyncio
from src.models.specie import Specie, SpecieResponse, SpecieListResponse, SpecieListItem, PlanetSummary, PeopleSummary
from src.services.swapi_client import SWAPIClient

class SpecieService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def _extract_id(self, url: str) -> int:
        return int(url.rstrip('/').split('/')[-1])

    async def get_specie_enriched(self, specie_id: int) -> SpecieResponse:
        raw_data = await self.swapi_client.get(f"/species/{specie_id}/")
        specie = Specie(**raw_data)
        homeworld_data = await self.swapi_client.get(specie.homeworld) if specie.homeworld else None
        people_data = await asyncio.gather(*[self.swapi_client.get(people_url) for people_url in specie.people])

        return SpecieResponse(
            id=specie_id,
            name=specie.name,
            classification=specie.classification,
            designation=specie.designation,
            average_height=specie.average_height,
            average_lifespan=specie.average_lifespan,
            eye_colors=specie.eye_colors,
            hair_colors=specie.hair_colors,
            skin_colors=specie.skin_colors,
            language=specie.language,
            homeworld=PlanetSummary(
                id=self._extract_id(homeworld_data['url']),
                name=homeworld_data['name'],
                climate=homeworld_data['climate'],
                terrain=homeworld_data['terrain']
            ) if homeworld_data else None,
            people=[
                PeopleSummary(
                    id=self._extract_id(person['url']),
                    name=person['name']
                ) for person in people_data
            ],
            statistics={
                "total_people": len(people_data),
                "appearance_in_movies": len(specie.films)
            }
        )

    async def get_species_list(self, page: int = 1) -> SpecieListResponse:
        raw_data = await self.swapi_client.get("/species/", params={"page": page})
        results = []

        for specie_data in raw_data['results']:
            specie = Specie(**specie_data)
            results.append(SpecieListItem(
                id=self._extract_id(specie.url),
                name=specie.name,
                classification=specie.classification,
                designation=specie.designation,
                language=specie.language
            ))
        
        return SpecieListResponse(
            count=raw_data['count'],
            next=raw_data.get('next'),
            previous=raw_data.get('previous'),
            results=results
        )