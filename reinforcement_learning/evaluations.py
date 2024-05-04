from typing import List, Tuple, Optional

from reinforcement_learning.types import PlacedBet, BetType, Action


def sum_back_bets(back_bets: List[PlacedBet]) -> Optional[PlacedBet]:
    if len(back_bets) == 0:
        return None

    back_stakes = sum(back_bet.stake for back_bet in back_bets)
    back_revenues = sum(back_bet.stake * back_bet.odds for back_bet in back_bets)

    back_odds = back_revenues / back_stakes
    return PlacedBet(
        bet_type=BetType.BACK,
        stake=back_stakes,
        odds=back_odds,
        minute=None,
    )


def sum_lay_bets(lay_bets: List[PlacedBet]) -> Optional[PlacedBet]:
    if len(lay_bets) == 0:
        return None

    lay_stakes = sum(lay_bet.stake for lay_bet in lay_bets)
    lay_incomes = sum(lay_bet.stake / (lay_bet.odds - 1) for lay_bet in lay_bets)
    lay_revenues = lay_stakes + lay_incomes

    lay_odds = lay_revenues / lay_incomes
    return PlacedBet(
        bet_type=BetType.LAY,
        stake=lay_stakes,
        odds=lay_odds,
        minute=None,
    )


def count_income_back_lay(back_bet: PlacedBet, lay_bet: PlacedBet) -> Tuple[float, float]:

    if back_bet is None:
        back_income = 0
    else:
        back_revenue = back_bet.stake * back_bet.odds
        back_income = back_revenue - back_bet.stake

    if lay_bet is None:
        lay_income = 0
    else:
        lay_income = lay_bet.stake / (lay_bet.odds - 1)

    return back_income, lay_income


def count_earnings_back_lay(back_bet: PlacedBet, lay_bet: PlacedBet) -> Tuple[float, float]:
    back_income, lay_income = count_income_back_lay(back_bet, lay_bet)

    back_earnings = back_income - (lay_bet.stake if lay_bet is not None else 0)
    lay_earnings = lay_income - (back_bet.stake if back_bet is not None else 0)

    return back_earnings, lay_earnings


def count_earnings_back_lay_from_summed_bets(placed_bets: List[PlacedBet]) -> Tuple[float, float]:
    back_bet, lay_bet = get_summed_back_lay_bets(placed_bets)
    return count_earnings_back_lay(back_bet, lay_bet)


def get_back_stake_for_surebet(back_earnings: float, lay_earnings: float, current_back_odds: float) -> float:
    return round((lay_earnings - back_earnings) / current_back_odds, 2)


def get_lay_stake_for_surebet(back_earnings: float, lay_earnings: float, current_lay_odds: float) -> float:
    return round((back_earnings - lay_earnings) * (current_lay_odds - 1) / current_lay_odds, 2)


def get_summed_back_lay_bets(placed_bets: List[PlacedBet]) -> (PlacedBet, PlacedBet):
    back_bet = None
    back_bets = [placed_bet for placed_bet in placed_bets if placed_bet.bet_type == BetType.BACK]
    if len(back_bets) > 0:
        back_bet = sum_back_bets(back_bets)

    lay_bet = None
    lay_bets = [placed_bet for placed_bet in placed_bets if placed_bet.bet_type == BetType.LAY]
    if len(lay_bets) > 0:
        lay_bet = sum_lay_bets(lay_bets)

    return back_bet, lay_bet


def get_surebet_stake(
        back_earnings: float,
        lay_earnings: float,
        back_price: float,
        lay_price: float
) -> Tuple[float, BetType]:
    if back_earnings < lay_earnings:
        surebet_stake = get_back_stake_for_surebet(
            back_earnings,
            lay_earnings,
            back_price,
        )
        return surebet_stake, BetType.BACK

    if back_earnings > lay_earnings:
        surebet_stake = get_lay_stake_for_surebet(
            back_earnings,
            lay_earnings,
            lay_price,
        )
        return surebet_stake, BetType.LAY

    return 0, BetType.BACK


def get_surebet(placed_bets: List[PlacedBet], back_price: float, lay_price: float) -> PlacedBet:
    back_earnings, lay_earnings = (
        count_earnings_back_lay_from_summed_bets(placed_bets)
    )
    stake, bet_type = get_surebet_stake(
        back_earnings,
        lay_earnings,
        back_price,
        lay_price
    )
    return PlacedBet(
        bet_type,
        stake,
        back_price if bet_type == BetType.BACK else lay_price,
        None
    )


def count_earnings(placed_bets: List[PlacedBet], back_price: float, lay_price: float) -> float:
    back_earnings, lay_earnings = count_earnings_back_lay_from_summed_bets(placed_bets)
    earnings = 0
    surebet_stake, bet_type = get_surebet_stake(back_earnings, lay_earnings, back_price, lay_price)

    if bet_type == BetType.BACK:
        surebet_revenue = surebet_stake * back_price
        surebet_income = surebet_revenue - surebet_stake
        earnings = back_earnings + surebet_income

    if bet_type == BetType.LAY:
        surebet_stake = get_lay_stake_for_surebet(
            back_earnings,
            lay_earnings,
            lay_price,
        )
        surebet_income = surebet_stake / (lay_price - 1)
        earnings = lay_earnings + surebet_income

    return round(earnings, 2)


def get_action_from_bet_type(bet_type: BetType, previous_bets: List[PlacedBet]) -> Action:
    back_earnings, lay_earnings = count_earnings_back_lay_from_summed_bets(previous_bets)

    if back_earnings == lay_earnings:
        return Action.BUY

    if back_earnings < lay_earnings:
        if bet_type == BetType.BACK:
            return Action.SETTLE
        else:
            return Action.BUY

    if back_earnings > lay_earnings:
        if bet_type == BetType.BACK:
            return Action.BUY
        else:
            return Action.SETTLE


def get_bet_type_from_action(action: Action, previous_bets: List[PlacedBet]) -> BetType:
    back_earnings, lay_earnings = count_earnings_back_lay_from_summed_bets(previous_bets)
    if back_earnings < lay_earnings:
        if action == Action.BUY:
            return BetType.LAY
        else:
            return BetType.BACK
    else:
        if action == Action.BUY:
            return BetType.BACK
        else:
            return BetType.LAY


def update_potential_liability(
        potential_liability: float,
        match_cash: float,
        previous_bets: List[PlacedBet],
        current_bet: PlacedBet = None
) -> float:
    if current_bet is None:
        return potential_liability

    action = get_action_from_bet_type(current_bet.bet_type, previous_bets)

    if action == Action.BUY:
        potential_liability -= current_bet.stake
    else:
        previous_bets_copy = previous_bets.copy()
        previous_bets_copy.append(current_bet)
        back_bet, lay_bet = get_summed_back_lay_bets(previous_bets_copy)
        back_earnings, lay_earnings = count_earnings_back_lay(back_bet, lay_bet)
        min_earnings = min(back_earnings, lay_earnings)
        potential_liability = match_cash + min_earnings

    if potential_liability < 0:
        print("WARNING: Not enough cash!")

    return round(potential_liability, 2)


