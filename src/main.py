from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from src.services.people_service import PeopleService

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.people_service = PeopleService()
    
    yield
    
    await app.state.people_service.swapi_client.close()

app = FastAPI(
    title="Case técnico com SWAPI",
    lifespan=lifespan
)

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