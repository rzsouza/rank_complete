from dataclasses import dataclass
from datetime import datetime


@dataclass
class Match:
    home_team:str
    home_team_score:int
    away_team:str
    away_team_score:int
    date: datetime
