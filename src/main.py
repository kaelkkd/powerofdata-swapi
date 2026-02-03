import aiohttp
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from src.services import (
    PeopleService,
    FilmService,
    PlanetService,
    SpecieService,
    StarshipService,
    VehicleService,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.people_service = PeopleService()
    app.state.film_service = FilmService()
    app.state.planet_service = PlanetService()
    app.state.specie_service = SpecieService()
    app.state.starship_service = StarshipService()
    app.state.vehicle_service = VehicleService()
    
    yield
    
    await app.state.people_service.swapi_client.close()
    await app.state.film_service.swapi_client.close()
    await app.state.film_service.swapi_client.close()
    await app.state.specie_service.swapi_client.close()
    await app.state.starship_service.swapi_client.close()

app = FastAPI(
    title="Case técnico com SWAPI",
    lifespan=lifespan,
    version="0.1.0"
)

##Health para CI/CD
@app.get("/health", tags=["System"])
async def health_check():
    swapi_status = "healthy"
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5.0)) as client:
            async with client.get("https://swapi.dev/api/") as response:
                if response.status != 200:
                    swapi_status = "degraded"
    except Exception:
        swapi_status = "unhealthy"
    
    return {
        "status": "healthy" if swapi_status == "healthy" else "degraded",
        "service": "star-wars-api",
        "version": "0.1.0",
        "dependencies": {
            "swapi": swapi_status
        }
    }

##Roor
@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Star Wars API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "characters": "/people/{id}",
            "planets": "/planets/{id}",
            "films": "/films/{id}",
            "starships": "/starships/{id}",
            "vehicles": "vehicles/{id}"
        }
    }

@app.get(
    "/people/{people_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por personagem",
    response_description="Informações customizdas"
)
async def get_person(people_id: int):
    try:
        return await app.state.people_service.get_people_enriched(people_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem de ID {people_id} não encontrado"
        )
    
##Filmes
@app.get(
    "/films/{film_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por filme",
    response_description="Informações customizadas sobre um filme"
)
async def get_film(film_id: int):
    try:
        return await app.state.film_service.get_film_enriched(film_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme de ID {film_id} não encontrado"
        )
    
##Planetas
@app.get(
    "/planets/{planet_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por planeta",
    response_description="Informações customizadas sobre um planeta"
)
async def get_planet(planet_id: int):
    try:
        return await app.state.planet_service.get_planet_enriched(planet_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planeta de ID {planet_id} não encontrado"
        )

##Species
@app.get(
    "/species/{specie_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por espécie",
    response_description="Informações customizadas sobre uma espécie"
)
async def get_specie(specie_id: int):
    try:
        return await app.state.specie_service.get_specie_enriched(specie_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Espécie de ID {specie_id} não encontrada"
        )

##Naves
@app.get(
    "/starships/{starship_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por nave",
    response_description="Informações customizadas sobre uma nave"
)
async def get_starship(starship_id: int):
    try:
        return await app.state.starship_service.get_starship_enriched(starship_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nave de ID {starship_id} não encontrada"
        )
    
##Veiculos
@app.get(
    "/vehicles/{vehicle_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por veículo",
    response_description="Informações customizadas sobre um veículo"
)
async def get_vehicle(vehicle_id: int):
    try:
        return await app.state.vehicle_service.get_vehicle_enriched(vehicle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veículo de ID {vehicle_id} não encontrado"
        )
           