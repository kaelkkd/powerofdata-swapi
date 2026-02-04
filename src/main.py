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

app = FastAPI(
    title="Case técnico com SWAPI",
    version="1.0.0"
)

async def get_state():
    if not hasattr(app.state, "services_initialized"):
        app.state.people_service = PeopleService()
        app.state.film_service = FilmService()
        app.state.planet_service = PlanetService()
        app.state.specie_service = SpecieService()
        app.state.starship_service = StarshipService()
        app.state.vehicle_service = VehicleService()
        app.state.services_initialized = True

    return app.state

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
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "people": {
                "list": "/people?page=1",
                "detail": "/people/{id}"
            },
            "planets": {
                "list": "/planets?page=1",
                "detail": "/planets/{id}"
            },
            "films": {
                "list": "/films?page=1",
                "detail": "/films/{id}"
            },
            "species": {
                "list": "/species?page=1",
                "detail": "/species/{id}"
            },
            "starships": {
                "list": "/starships?page=1",
                "detail": "/starships/{id}"
            },
            "vehicles": {
                "list": "/vehicles?page=1",
                "detail": "/vehicles/{id}"
            }
        }
    }

##People
@app.get(
    "/people",
    status_code=status.HTTP_200_OK,
    summary="Lista de personagens",
    response_description="Lista paginada de personagens"
)
async def get_people_list(page: int = 1):
    state = await get_state()
    try:
        return await app.state.people_service.get_people_list(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao buscar lista de personagens"
        )

@app.get(
    "/people/{people_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por personagem",
    response_description="Informações customizdas"
)
async def get_person(people_id: int):
    state = await get_state()
    try:
        return await app.state.people_service.get_people_enriched(people_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem de ID {people_id} não encontrado"
        )
    
##Filmes
@app.get(
    "/films",
    status_code=status.HTTP_200_OK,
    summary="Lista de filmes",
    response_description="Lista paginada de filmes"
)
async def get_films_list(page: int = 1):
    state = await get_state()
    try:
        return await app.state.film_service.get_films_list(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao buscar lista de filmes"
        )

@app.get(
    "/films/{film_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por filme",
    response_description="Informações customizadas sobre um filme"
)
async def get_film(film_id: int):
    state = await get_state()
    try:
        return await app.state.film_service.get_film_enriched(film_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme de ID {film_id} não encontrado"
        )
    
##Planetas
@app.get(
    "/planets",
    status_code=status.HTTP_200_OK,
    summary="Lista de planetas",
    response_description="Lista paginada de planetas"
)
async def get_planets_list(page: int = 1):
    state = await get_state()
    try:
        return await app.state.planet_service.get_planets_list(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao buscar lista de planetas"
        )

@app.get(
    "/planets/{planet_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por planeta",
    response_description="Informações customizadas sobre um planeta"
)
async def get_planet(planet_id: int):
    state = await get_state()
    try:
        return await app.state.planet_service.get_planet_enriched(planet_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planeta de ID {planet_id} não encontrado"
        )

##Species
@app.get(
    "/species",
    status_code=status.HTTP_200_OK,
    summary="Lista de espécies",
    response_description="Lista paginada de espécies"
)
async def get_species_list(page: int = 1):
    state = await get_state()
    try:
        return await app.state.specie_service.get_species_list(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao buscar lista de espécies"
        )

@app.get(
    "/species/{specie_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por espécie",
    response_description="Informações customizadas sobre uma espécie"
)
async def get_specie(specie_id: int):
    state = await get_state()
    try:
        return await app.state.specie_service.get_specie_enriched(specie_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Espécie de ID {specie_id} não encontrada"
        )

##Naves
@app.get(
    "/starships",
    status_code=status.HTTP_200_OK,
    summary="Lista de naves",
    response_description="Lista paginada de naves"
)
async def get_starships_list(page: int = 1):
    state = await get_state()
    try:
        return await app.state.starship_service.get_starships_list(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao buscar lista de naves"
        )

@app.get(
    "/starships/{starship_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por nave",
    response_description="Informações customizadas sobre uma nave"
)
async def get_starship(starship_id: int):
    state = await get_state()
    try:
        return await app.state.starship_service.get_starship_enriched(starship_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nave de ID {starship_id} não encontrada"
        )

##Veiculos
@app.get(
    "/vehicles",
    status_code=status.HTTP_200_OK,
    summary="Lista de veículos",
    response_description="Lista paginada de veículos"
)
async def get_vehicles_list(page: int = 1):
    state = await get_state()
    try:
        return await app.state.vehicle_service.get_vehicles_list(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao buscar lista de veículos"
        )
    
@app.get(
    "/vehicles/{vehicle_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca por veículo",
    response_description="Informações customizadas sobre um veículo"
)
async def get_vehicle(vehicle_id: int):
    state = await get_state()
    try:
        return await app.state.vehicle_service.get_vehicle_enriched(vehicle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veículo de ID {vehicle_id} não encontrado"
        )
           