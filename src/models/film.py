from datetime import date
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Film(BaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: date
    species: List[str]
    starships: List[str]
    vehicles: List[str]
    characters: List[str]
    planets: List[str]
    url: str
    created: str
    edited: str

class PlanetSummary(BaseModel):
    id: int
    name: str
    climate: str
    terrain: str

class FilmResponse(BaseModel):
    id: int
    title: str
    director: str
    producer: str
    opening_crawl: str
    release_date: date
    planets: List[PlanetSummary]
    statistics: Dict[str, int] = Field(description="Estatísticas gerais")

class FilmListItem(BaseModel):
    id: int
    title: str
    episode_id: int
    director: str
    release_date: date

class FilmListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[FilmListItem]


