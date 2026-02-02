from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class Vehicle(BaseModel):
    name: str
    model: str
    vehicle_class: str
    manufacturer: str
    length: str
    cost_in_credits: str
    crew: str
    passengers: str
    max_atmosphering_speed: str
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

class VehicleResponse(BaseModel):
    id: int
    name: str
    model: str
    vehicle_class: str
    manufacturer: str
    length: Optional[float] = Field(None, description="Comprimento em metros")
    cost_in_credits: Optional[int] = Field(None, description="Custo em créditos galácticos")
    crew: Optional[int] = Field(None, description="Número de tripulantes")
    passengers: Optional[int] = Field(None, description="Número de passageiros")
    max_atmosphering_speed: str
    cargo_capacity: Optional[int] = Field(None, description="Capacidade de carga em kg")
    consumables: Optional[str] = Field(None, description="Tempo de duração de suprimentos")
    pilots: List[PeopleSummary]
    films: List[FilmSummary]
    statistics: Dict[str, int] = Field(description="Estatísticas gerais")

    @field_validator('length', mode='before')
    def parse_length(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    @field_validator('cost_in_credits', mode='before')
    def parse_cost_in_credits(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
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

    @field_validator('cargo_capacity', mode='before')
    def parse_cargo_capacity(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None