import math
from typing import List

import pandas as pd
from pandas import DataFrame

from reinforcement_learning import evaluations
from reinforcement_learning.types import Comparison, Individual, State, Parameter, StateDetails, \
    Strategy, PlacedBet, BetType
from models.market import MarketKeys


def place_bet(
        potential_liability: float,
        strategy: Strategy,
        placed_bets: List[PlacedBet],
        match_state: pd.Series
) -> PlacedBet:

    back_price = match_state[MarketKeys.home_back_1_price.value]
    lay_price = match_state[MarketKeys.home_lay_1_price.value]

    bet_type = evaluations.get_bet_type_from_action(strategy.action, placed_bets)
    stake = potential_liability * strategy.stake_percentage
    stake = math.floor(stake * 100) / 100

    if bet_type == BetType.BACK:
        odds = back_price
    else:
        odds = lay_price

    return PlacedBet(
        bet_type=bet_type,
        stake=stake,
        odds=odds,
        minute=match_state[MarketKeys.minutes_to_match.value],
    )


def get_state_details_from_list(state_details: List[StateDetails], state_name: State) -> StateDetails:
    for state_detail in state_details:
        if state_detail.name == state_name:
            return state_detail


def calculate_average_stake_or_reset(parameters: List[Parameter], states: List[StateDetails]) -> float:
    stake_value = 0

    for param in parameters:
        if param.comparison == Comparison.OVER:
            condition_met = param.value >= get_state_details_from_list(states, param.name).value
        elif param.comparison == Comparison.UNDER:
            condition_met = param.value <= get_state_details_from_list(states, param.name).value
        else:
            condition_met = False

        if condition_met:
            stake_value = (stake_value + param.money_share) / 2
        else:
            stake_value = 0
            break

    return stake_value


def get_strategy_stake_percentage(strategy: Strategy, states: List[StateDetails]) -> Strategy:
    strategy.stake_percentage = calculate_average_stake_or_reset(strategy.parameters, states)
    return strategy


def choose_best_strategy(strategies: List[Strategy]) -> Strategy:
    if not strategies:
        raise ValueError("Empty list of strategies")

    max_stake_percentage_strategy = max(
        strategies,
        key=lambda obj: obj.stake_percentage if hasattr(obj, 'stake_percentage') else float('-inf')
    )

    if not hasattr(max_stake_percentage_strategy, 'stake_percentage'):
        raise ValueError("Bet object does not have the 'stake_percentage' attribute")

    return max_stake_percentage_strategy


def refresh_minute(state: StateDetails, match_state: pd.Series) -> StateDetails:
    state.value = match_state[MarketKeys.minutes_to_match.value]
    return state


def refresh_potential_liability(
        state: StateDetails,
        cash: float,
        previous_bets: List[PlacedBet],
        current_bet: PlacedBet
) -> StateDetails:
    state.value = evaluations.update_potential_liability(
        state.value,
        cash,
        previous_bets,
        current_bet
    )
    return state


def refresh_earnings(state: StateDetails, placed_bets: List[PlacedBet], match_state: pd.Series) -> StateDetails:
    back_price = match_state[MarketKeys.home_back_1_price.value]
    lay_price = match_state[MarketKeys.home_lay_1_price.value]
    state.value = evaluations.count_earnings(placed_bets, back_price, lay_price)
    return state


def refresh_cash(cash: float, placed_bets: List[PlacedBet], match_state: pd.Series) -> float:
    back_price = match_state[MarketKeys.home_back_1_price.value]
    lay_price = match_state[MarketKeys.home_lay_1_price.value]
    cash += evaluations.count_earnings(placed_bets, back_price, lay_price)
    return cash


def refresh_current_state(
        match_state: pd.Series,
        states: List[StateDetails],
        previous_bets: List[PlacedBet],
        cash: float,
        current_bet: PlacedBet = None,
) -> List[StateDetails]:
    new_states = []

    minute_state = get_state_details_from_list(states, State.MINUTE)
    potential_liability_state = get_state_details_from_list(states, State.POTENTIAL_LIABILITY)
    earnings_state = get_state_details_from_list(states, State.EARNINGS)

    new_minute_state = refresh_minute(minute_state, match_state)
    new_potential_liability_state = refresh_potential_liability(
        potential_liability_state,
        cash,
        previous_bets,
        current_bet
    )
    new_earnings_state = refresh_earnings(earnings_state, previous_bets + [current_bet], match_state)

    new_states.append(new_minute_state)
    new_states.append(new_potential_liability_state)
    new_states.append(new_earnings_state)

    return new_states


def get_updated_available_strategies(strategies: List[Strategy], used_strategy: Strategy) -> List[Strategy]:
    return [obj for obj in strategies if obj.id != used_strategy.id]


def is_match_ending(match_index, match: DataFrame) -> bool:
    return match.loc[match_index, MarketKeys.minutes_to_match.value] == 0


def bet_matches(population: List[Individual], matches: List[DataFrame]) -> List[Individual]:
    for match in matches:
        for index, match_state in match.iterrows():
            for individual in population:
                strategies_with_stake = []

                for strategy in individual.available_strategies:
                    strategies_with_stake.append(get_strategy_stake_percentage(strategy, individual.states))

                best_strategy = choose_best_strategy(strategies_with_stake) if len(strategies_with_stake) > 0 else None
                potential_liability = get_state_details_from_list(individual.states, State.POTENTIAL_LIABILITY).value

                if is_match_ending(index, match):
                    individual.cash = refresh_cash(individual.cash, individual.placed_bets, match_state)
                    individual.placed_bets_number += len(individual.placed_bets)
                    individual.available_strategies = individual.strategies.copy()
                    individual.placed_bets = []
                else:
                    if best_strategy is not None and best_strategy.stake_percentage != 0:
                        placed_bet = place_bet(potential_liability, best_strategy, individual.placed_bets, match_state)

                        if placed_bet.stake > 0:
                            refresh_current_state(
                                match_state,
                                individual.states,
                                individual.placed_bets,
                                individual.cash,
                                placed_bet
                            )
                            individual.placed_bets.append(placed_bet)
                            individual.available_strategies = get_updated_available_strategies(
                                individual.available_strategies,
                                best_strategy,
                            )

    return population
