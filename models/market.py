from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class Market:
    minutes_to_match: int
    last_match_time: datetime
    total_matched: float
    total_available: float

    home_last_price_traded: float
    away_last_price_traded: float
    draw_last_price_traded: float

    home_back_1_price: float
    home_back_2_price: float
    home_back_3_price: float

    away_back_1_price: float
    away_back_2_price: float
    away_back_3_price: float

    draw_back_1_price: float
    draw_back_2_price: float
    draw_back_3_price: float

    home_back_1_size: float
    home_back_2_size: float
    home_back_3_size: float

    away_back_1_size: float
    away_back_2_size: float
    away_back_3_size: float

    draw_back_1_size: float
    draw_back_2_size: float
    draw_back_3_size: float

    home_lay_1_price: float
    home_lay_2_price: float
    home_lay_3_price: float

    away_lay_1_price: float
    away_lay_2_price: float
    away_lay_3_price: float

    draw_lay_1_price: float
    draw_lay_2_price: float
    draw_lay_3_price: float

    home_lay_1_size: float
    home_lay_2_size: float
    home_lay_3_size: float

    away_lay_1_size: float
    away_lay_2_size: float
    away_lay_3_size: float

    draw_lay_1_size: float
    draw_lay_2_size: float
    draw_lay_3_size: float


class MarketKeys(Enum):
    minutes_to_match = 'minutes_to_match'
    last_match_time = 'last_match_time'
    total_matched = 'total_matched'
    total_available = 'total_available'

    home_last_price_traded = 'home_last_price_traded'
    away_last_price_traded = 'away_last_price_traded'
    draw_last_price_traded = 'draw_last_price_traded'

    home_back_1_price = 'home_back_1_price'
    home_back_2_price = 'home_back_2_price'
    home_back_3_price = 'home_back_3_price'
    away_back_1_price = 'away_back_1_price'
    away_back_2_price = 'away_back_2_price'
    away_back_3_price = 'away_back_3_price'
    draw_back_1_price = 'draw_back_1_price'
    draw_back_2_price = 'draw_back_2_price'
    draw_back_3_price = 'draw_back_3_price'

    home_back_1_size = 'home_back_1_size'
    home_back_2_size = 'home_back_2_size'
    home_back_3_size = 'home_back_3_size'
    away_back_1_size = 'away_back_1_size'
    away_back_2_size = 'away_back_2_size'
    away_back_3_size = 'away_back_3_size'
    draw_back_1_size = 'draw_back_1_size'
    draw_back_2_size = 'draw_back_2_size'
    draw_back_3_size = 'draw_back_3_size'

    home_lay_1_price = 'home_lay_1_price'
    home_lay_2_price = 'home_lay_2_price'
    home_lay_3_price = 'home_lay_3_price'
    away_lay_1_price = 'away_lay_1_price'
    away_lay_2_price = 'away_lay_2_price'
    away_lay_3_price = 'away_lay_3_price'
    draw_lay_1_price = 'draw_lay_1_price'
    draw_lay_2_price = 'draw_lay_2_price'
    draw_lay_3_price = 'draw_lay_3_price'

    home_lay_1_size = 'home_lay_1_size'
    home_lay_2_size = 'home_lay_2_size'
    home_lay_3_size = 'home_lay_3_size'
    away_lay_1_size = 'away_lay_1_size'
    away_lay_2_size = 'away_lay_2_size'
    away_lay_3_size = 'away_lay_3_size'
    draw_lay_1_size = 'draw_lay_1_size'
    draw_lay_2_size = 'draw_lay_2_size'
    draw_lay_3_size = 'draw_lay_3_size'

