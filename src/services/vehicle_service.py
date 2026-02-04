import asyncio
from src.models.vehicle import Vehicle, VehicleResponse, VehicleListResponse, VehicleListItem, PeopleSummary, FilmSummary
from src.services.swapi_client import SWAPIClient

class VehicleService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def _extract_id(self, url: str) -> int:
        return int(url.rstrip('/').split('/')[-1])

    async def get_vehicle_enriched(self, vehicle_id: int) -> VehicleResponse:
        raw_data = await self.swapi_client.get(f"/vehicles/{vehicle_id}/")
        vehicle = Vehicle(**raw_data)
        pilots_data = await asyncio.gather(*[self.swapi_client.get(pilot_url) for pilot_url in vehicle.pilots])
        films_data = await asyncio.gather(*[self.swapi_client.get(film_url) for film_url in vehicle.films])

        return VehicleResponse(
            id=vehicle_id,
            name=vehicle.name,
            model=vehicle.model,
            vehicle_class=vehicle.vehicle_class,
            manufacturer=vehicle.manufacturer,
            length=vehicle.length,
            cost_in_credits=vehicle.cost_in_credits,
            crew=vehicle.crew,
            passengers=vehicle.passengers,
            max_atmosphering_speed=vehicle.max_atmosphering_speed,
            cargo_capacity=vehicle.cargo_capacity,
            consumables=vehicle.consumables,
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

    async def get_vehicles_list(self, page: int = 1) -> VehicleListResponse:
        raw_data = await self.swapi_client.get("/vehicles/", params={"page": page})
        results = []

        for vehicle_data in raw_data['results']:
            vehicle = Vehicle(**vehicle_data)
            results.append(VehicleListItem(
                id=self._extract_id(vehicle.url),
                name=vehicle.name,
                model=vehicle.model,
                vehicle_class=vehicle.vehicle_class,
                manufacturer=vehicle.manufacturer
            ))
        
        return VehicleListResponse(
            count=raw_data['count'],
            next=raw_data.get('next'),
            previous=raw_data.get('previous'),
            results=results
        )