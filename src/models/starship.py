from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class Starship(BaseModel):
    name: str
    model: str
    starship_class: str
    manufacturer: str
    cost_in_credits: str
    length: str
    crew: str
    passengers: str
    max_atmosphering_speed: str
    hyperdrive_rating: str
    MGLT: str
    cargo_capacity: str
    consumables: str
    films: List[str]
    pilots: List[str]
    url: str
    created: str
    edited: str

class PeopleSummary(BaseModel):
    id: int
    name: str
    specie: str

class FilmSummary(BaseModel):
    id: int
    title: str
    episode_id: int
    release_date: str

class StarshipResponse(BaseModel):
    id: int
    name: str
    model: str
    starship_class: str
    manufacturer: str
    cost_in_credits: Optional[int] = Field(None, description="Custo em créditos galácticos")
    length: Optional[float] = Field(None, description="Comprimento em metros")
    crew: Optional[int] = Field(None, description="Número de tripulantes")
    passengers: Optional[int] = Field(None, description="Número de passageiros")
    max_atmosphering_speed: Optional[str] = Field(None, description="Velocidade máxima na atmosfera")
    hyperdrive_rating: Optional[float] = Field(None, description="Classificação do hiperdrive")
    MGLT: Optional[int] = Field(None, description="Velocidade máxima em MGLT(Megalights)")
    cargo_capacity: Optional[int] = Field(None, description="Capacidade de carga em kg")
    consumables: str
    pilots: List[PeopleSummary]
    films: List[FilmSummary]
    statistics: Dict[str, int] = Field(description="Estatísticas gerais")

    @field_validator('cost_in_credits', mode='before')
    def parse_cost_in_credits(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('length', mode='before')
    def parse_length(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    @field_validator('crew', mode='before')
    def parse_crew(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('passengers', mode='before')
    def parse_passengers(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('hyperdrive_rating', mode='before')
    def parse_hyperdrive_rating(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    @field_validator('MGLT', mode='before')
    def parse_MGLT(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('cargo_capacity', mode='before')
    def parse_cargo_capacity(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None