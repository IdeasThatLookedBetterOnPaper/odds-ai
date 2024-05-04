from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, TypeVar

EnumGeneric = TypeVar('EnumGeneric', bound=Enum)


class Action(Enum):
    BUY = 'Buy'
    SETTLE = 'Settle'


class BetType(Enum):
    LAY = 'Lay'
    BACK = 'Back'


class Comparison(Enum):
    OVER = 'Over'
    UNDER = 'Under'


class State(Enum):
    MINUTE = 'Minute'
    EARNINGS = 'Earnings'
    POTENTIAL_LIABILITY = 'Potential liability'


@dataclass()
class StateDetails:
    name: State
    value: float
    min: float
    max: float


@dataclass()
class Parameter:
    name: State
    value: float
    comparison: Comparison
    money_share: float


@dataclass()
class Strategy:
    id: int
    parameters: List[Parameter]
    action: Action
    stake_percentage: float


@dataclass()
class PlacedBet:
    bet_type: BetType
    stake: float
    odds: float
    minute: Optional[float]


@dataclass()
class Individual:
    states: List[StateDetails]
    strategies: List[Strategy]
    available_strategies: List[Strategy]
    placed_bets: List[PlacedBet]
    cash: float
    placed_bets_number: int
