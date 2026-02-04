from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class Specie(BaseModel):
    name: str
    classification: str
    designation: str
    average_height: str
    average_lifespan: str
    eye_colors: str
    hair_colors: str
    skin_colors: str
    language: str
    homeworld: Optional[str] = None
    people: List[str]
    films: List[str]
    url: str
    created: str
    edited: str

class PlanetSummary(BaseModel):
    id: int
    name: str
    climate: str
    terrain: str

class PeopleSummary(BaseModel):
    id: int
    name: str

class SpecieResponse(BaseModel):
    id: int
    name: str
    classification: str
    designation: str
    average_height: Optional[int] = Field(None, description="Altura média em centímetros")
    average_lifespan: Optional[int] = Field(None, description="Expectativa de vida média em anos")
    eye_colors: str
    hair_colors: Optional[str] = Field(None, description="Cores de cabelo")
    skin_colors: str
    language: Optional[str] = Field(None, description="Idioma falado")
    homeworld: Optional[PlanetSummary] = Field(None, description="Planeta de origem")
    people: List[PeopleSummary]
    statistics: Dict[str, int] = Field(description="Estatísticas gerais")

    @field_validator('average_height', mode='before')
    def parse_average_height(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('average_lifespan', mode='before')
    def parse_average_lifespan(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

class SpecieListItem(BaseModel):
    id: int
    name: str
    classification: str
    designation: str
    language: Optional[str] = Field(None, description="Idioma falado")

class SpecieListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[SpecieListItem]