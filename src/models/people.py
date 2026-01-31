from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class People(BaseModel):
    name: str
    birth_year: str
    eye_color: str
    gender: str
    hair_color: str
    height: str
    mass: str
    skin_color: str
    homeworld: str
    films: List[str]
    species: List[str]
    starships: List[str]
    vehicles: List[str]
    url: str
    created: str
    edited: str

class PlanetSummary(BaseModel):
    id: int
    name: str
    climate: str
    terrain: str

class FilmSummary(BaseModel):
    id: int
    title: str
    episode_id: int
    release_date: str

class PeopleResponse(BaseModel):
    id: int
    name: str
    height: Optional[int] = Field(None, description="Altura em centimetros")
    mass: Optional[float] = Field(None, description="Massa em kilogramas")
    appearance: Dict[str, str] = Field(description="Caracteristicas fisicas")
    birth_year: str
    gender: str
    homeworld: PlanetSummary
    films: Optional[List[FilmSummary]] = Field(None, description="Aparicoes em filmes")
    statistics: Dict[str, int] = Field(description="Estatisticas")

    @field_validator('height', mode='before')
    def parse_height(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('mass', mode='before')
    def parse_mass(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None
    
