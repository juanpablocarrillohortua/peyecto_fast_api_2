from typing import Union
from pydantic import BaseModel, Field
from enum import Enum

class FaseOption(str, Enum):
    Group_stage = "Group stage"
    Semi_finals = "Semi-finals"
    Final = "Final"
    Round_of_16 = "Round of 16"
    Quarter_finals = "Quarter-finals"
    Third_place = "Third place"
    First_round = 'First round'
    Final_round = 'Final round'
    First_group_stage = 'First group stage'
    Second_group_stage = 'Second group stage'

class Partido(BaseModel):
   anyo: int = Field(gt=0)
   fase: FaseOption
   equipolocal: str
   goleslocales: int
   golesvisitante: int
   equipovisitante: str
   estaequipoanfitrion: bool