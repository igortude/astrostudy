from pydantic import BaseModel, Field
from typing import List

class CloseApproachData(BaseModel):
    close_approach_date: str
    relative_velocity_kps: float = Field(alias="relative_velocity", validation_alias="relative_velocity") # Simplificado para exemplo
    miss_distance_km: float = Field(alias="miss_distance", validation_alias="miss_distance") # Simplificado para exemplo

    class Config:
        populate_by_name = True

class AsteroidRecord(BaseModel):
    id: str
    name: str
    absolute_magnitude_h: float
    is_potentially_hazardous_asteroid: bool
    # Adicionar outros campos conforme necessário
