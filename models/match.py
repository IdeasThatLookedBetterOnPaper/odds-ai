from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class Match:
    event_id: str
    market_id: str
    open_date: datetime
    home_team: str
    away_team: str
    country_code: str


class MatchKeys(Enum):
    event_id = 'event_id'
    market_id = 'market_id'
    open_date = 'open_date'
    home_team = 'home_team'
    away_team = 'away_team'
    country_code = 'country_code'
