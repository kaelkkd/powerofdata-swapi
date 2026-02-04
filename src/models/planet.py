from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class Planet(BaseModel):
    name: str
    diameter: str
    rotation_period: str
    orbital_period: str
    gravity: str
    population: str
    climate: str
    terrain: str
    surface_water: str
    residents: List[str]
    films: List[str]
    url: str
    created: str
    edited: str

class PeopleSummary(BaseModel):
    id: int
    name: str

class FilmSummary(BaseModel):
    id: int
    title: str
    episode_id: int
    release_date: str

class PlanetResponse(BaseModel):
    id: int
    name: str
    diameter: Optional[int] = Field(None, description="Diâmetro em quilômetros")
    rotation_period: Optional[int] = Field(None, description="Período de rotação em horas")
    orbital_period: Optional[int] = Field(None, description="Período orbital em dias")
    gravity: Optional[float] = Field(None, description="Gravidade em Gs")
    population: Optional[int] = Field(None, description="População")
    climate: str
    terrain: str
    surface_water: Optional[float] = Field(None, description="Percentual de água na superfície")
    residents: List[PeopleSummary]
    films: List[FilmSummary]
    statistics: Dict[str, int] = Field(description="Estatísticas gerais")

    @field_validator('diameter', mode='before')
    def parse_diameter(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('rotation_period', mode='before')
    def parse_rotation_period(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('orbital_period', mode='before')
    def parse_orbital_period(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('gravity', mode='before')
    def parse_gravity(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    @field_validator('population', mode='before')
    def parse_population(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

    @field_validator('surface_water', mode='before')
    def parse_surface_water(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

class PlanetListItem(BaseModel):
    id: int
    name: str
    climate: str
    terrain: str
    population: Optional[int] = Field(None, description="População do planeta")

    @field_validator('population', mode='before')
    def parse_population(cls, v):
        if v == 'unknown' or not v:
            return None
        try:
            return int(v)
        except ValueError:
            return None

class PlanetListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PlanetListItem]