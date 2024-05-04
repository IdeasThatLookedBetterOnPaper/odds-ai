import unittest

from reinforcement_learning import evaluations
from reinforcement_learning.types import PlacedBet, BetType, Action


class TestCase(unittest.TestCase):
    back_bets = [
        PlacedBet(BetType.BACK, 10, 2.5, None),
        PlacedBet(BetType.BACK, 20, 3.1, None),
    ]
    lay_bets = [
        PlacedBet(BetType.LAY, 10, 2, None),
        PlacedBet(BetType.LAY, 20, 3, None),
    ]
    lay_bets2 = [
        PlacedBet(BetType.LAY, 25, 2, None),
        PlacedBet(BetType.LAY, 30, 3, None),
    ]
    back_price = 2.9
    lay_price = 2.3

    def test_sum_back_bets(self):
        result = evaluations.sum_back_bets(self.back_bets)
        self.assertEqual(PlacedBet(BetType.BACK, 30, 2.9, None), result)

    def test_sum_lay_bets(self):
        result = evaluations.sum_lay_bets(self.lay_bets)
        self.assertEqual(PlacedBet(BetType.LAY, 30, 2.5, None), result)

    def test_count_income_back_lay(self):
        summed_back_bets = evaluations.sum_back_bets(self.back_bets)
        summed_lay_bets = evaluations.sum_lay_bets(self.lay_bets)
        result = evaluations.count_income_back_lay(summed_back_bets, summed_lay_bets)
        self.assertEqual((57, 20), result)

    def test_count_earnings_back_lay(self):
        summed_back_bets = evaluations.sum_back_bets(self.back_bets)
        summed_lay_bets = evaluations.sum_lay_bets([])

        result = evaluations.count_earnings_back_lay(summed_back_bets, summed_lay_bets)
        self.assertEqual((57, -30), result)

        summed_lay_bets = evaluations.sum_lay_bets(self.lay_bets)
        result = evaluations.count_earnings_back_lay(summed_back_bets, summed_lay_bets)
        self.assertEqual((27, -10), result)

    def test_count_earnings_back_lay_from_summed_bets(self):
        bets = []
        bets.extend(self.back_bets)
        bets.extend(self.lay_bets)
        result = evaluations.count_earnings_back_lay_from_summed_bets(bets)
        self.assertEqual((27, -10), result)

    def test_get_back_stake_for_surebet(self):
        result = evaluations.get_back_stake_for_surebet(1, 13, 2.9)
        self.assertEqual(4.14, result)

    def test_get_lay_stake_for_surebet(self):
        result = evaluations.get_lay_stake_for_surebet(27, -10, 2.3)
        self.assertEqual(20.91, result)

    def test_get_summed_back_lay_bets(self):
        bets = []
        bets.extend(self.back_bets)
        bets.extend(self.lay_bets)
        result = evaluations.get_summed_back_lay_bets(bets)
        self.assertEqual((
            PlacedBet(BetType.BACK, 30, 2.9, None),
            PlacedBet(BetType.LAY, 30, 2.5, None)
        ), result)

    def test_get_surebet_stake(self):
        result = evaluations.get_surebet_stake(27, -10, self.back_price, self.lay_price)
        self.assertEqual((20.91, BetType.LAY), result)

    def test_count_earnings(self):
        placed_bets = []
        placed_bets.extend(self.back_bets)
        placed_bets.extend(self.lay_bets)

        result = evaluations.count_earnings(placed_bets, self.back_price, self.lay_price)

        self.assertEqual(6.08, result)

        placed_bets = []
        placed_bets.extend(self.back_bets)
        placed_bets.extend(self.lay_bets2)
        result = evaluations.count_earnings(placed_bets, self.back_price, self.lay_price)

        self.assertEqual(7.24, result)

    def test_get_action_from_bet_type(self):
        bets = []
        bets.extend(self.back_bets)
        bets.extend(self.lay_bets)

        result = evaluations.get_action_from_bet_type(BetType.BACK, bets)

        self.assertEqual(Action.BUY, result)

        bets = []
        bets.extend(self.back_bets)
        bets.extend(self.lay_bets2)

        result = evaluations.get_action_from_bet_type(BetType.BACK, bets)

        self.assertEqual(Action.SETTLE, result)

    def test_get_bet_type_from_action(self):
        bets = []
        bets.extend(self.back_bets)
        bets.extend(self.lay_bets)

        result = evaluations.get_bet_type_from_action(Action.BUY, bets)

        self.assertEqual(BetType.BACK, result)

        bets = []
        bets.extend(self.back_bets)
        bets.extend(self.lay_bets2)

        result = evaluations.get_bet_type_from_action(Action.SETTLE, bets)

        self.assertEqual(BetType.BACK, result)

    def test_update_potential_liability(self):
        back_bets = self. back_bets
        lay_bets = self.lay_bets

        cash_overtime = [90, 100, 85, 90]

        bets_overtime = [
            back_bets[0],
            lay_bets[0],
            lay_bets[1],
            back_bets[1]
        ]
        bets = []

        current_bet: PlacedBet
        match_cash = 100
        potential_liability = match_cash

        final_back_price = 2.5
        final_lay_price = 2

        def iterate(i: int):
            nonlocal current_bet, potential_liability

            current_bet = bets_overtime[i]
            potential_liability = evaluations.update_potential_liability(potential_liability, match_cash, bets, current_bet)
            bets.append(current_bet)

            self.assertEqual(cash_overtime[i], potential_liability)

        for index in range(len(bets_overtime)):
            iterate(index)

        def place_last_bet(cash_var: float) -> float:
            final_bet = evaluations.get_surebet(bets_overtime, final_back_price, final_lay_price)
            return evaluations.update_potential_liability(cash_var, match_cash, bets, final_bet)

        potential_liability = place_last_bet(potential_liability)

        expected_earnings = evaluations.count_earnings(bets_overtime, final_back_price, final_lay_price)

        self.assertEqual(100 + expected_earnings, potential_liability)
