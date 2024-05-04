import random
import statistics
import uuid
from typing import List, Type

from colorama import Fore, Style
from reinforcement_learning import betting
from reinforcement_learning.types import StateDetails, Strategy, EnumGeneric, Parameter, Comparison, State, \
    Individual, Action
from utils import data_transformation


def get_rand_value(min_value: float, max_value: float) -> float:
    return random.uniform(min_value, max_value)


def get_rand_enum_value(enum_class: Type[EnumGeneric]) -> EnumGeneric:
    return random.choice(list(enum_class))


def generate_parameters(states: List[StateDetails]) -> List[Parameter]:
    parameters = []

    for state in states:
        if state.name == State.MINUTE:
            name = state.name
            value = get_rand_value(state.min, state.max)
            comparison = get_rand_enum_value(Comparison)
            money_share = get_rand_value(0, 1)

            parameters.append(Parameter(name, value, comparison, money_share))

    return parameters


def generate_states() -> List[StateDetails]:
    return [
        StateDetails(State.MINUTE, 180, 0, 180),
        StateDetails(State.POTENTIAL_LIABILITY, 1000, 0, 1),
        StateDetails(State.EARNINGS, 0, -1, 10)
    ]


def generate_strategy(states: List[StateDetails]) -> Strategy:
    parameters = generate_parameters(states)
    action = random.choice(list(Action))
    unique_id = uuid.uuid4()

    return Strategy(id=unique_id.int, parameters=parameters, action=action, stake_percentage=0)


def generate_new_individual() -> Individual:
    states = generate_states()
    strategies = []

    for _ in range(0, int(get_rand_value(1, 10))):
        strategies.append(generate_strategy(states))

    return Individual(
        states=states,
        strategies=strategies,
        available_strategies=strategies,
        placed_bets=[],
        cash=0,
        placed_bets_number=0
    )


def crossover(parent1: Individual, parent2: Individual) -> Individual:
    genotype_length = min(len(parent1.strategies), len(parent2.strategies))
    crossover_point = random.randint(0, genotype_length - 1)
    child_genotype = parent1.strategies[:crossover_point] + parent2.strategies[crossover_point:]
    return Individual(
        states=[],
        strategies=child_genotype,
        available_strategies=child_genotype,
        placed_bets=[],
        cash=0,
        placed_bets_number=0
    )


def generate_children(population: List[Individual], child_ratio: float) -> List[Individual]:
    if child_ratio < 1:
        num_parents_with_children = int(len(population) * child_ratio)
        parents_with_children = random.sample(population, num_parents_with_children)
    else:
        parents_with_children = population

    children = []
    for parent in parents_with_children:
        num_children = int(child_ratio)
        if random.random() < child_ratio % 1:
            num_children += 1

        for _ in range(num_children):
            parent1, parent2 = random.sample(parents_with_children, 2)
            child = crossover(parent1, parent2)
            children.append(child)

    return children


def selection(population: List[Individual], percentage_selected: float) -> List[Individual]:
    num_selected = int(len(population) * percentage_selected)
    population = sorted(population, key=lambda x: x.cash)
    population = population[-num_selected:]
    return population


def roulette_wheel_selection(population: List[Individual], percentage_selected: float):
    selected_individuals = []

    total_cash = sum(individual.cash for individual in population)

    num_selected = int(len(population) * percentage_selected)

    for _ in range(num_selected):
        rand_value = random.uniform(0, total_cash)
        cumulative_cash = 0

        for individual in population:
            cumulative_cash += individual.cash
            if cumulative_cash >= rand_value:
                selected_individuals.append(individual)
                break

    return selected_individuals


def reset_population_states(population: List[Individual]) -> List[Individual]:
    for individual in population:
        individual.cash = 1000
        individual.states = generate_states()
        individual.placed_bets = []
    return population


def end_condition(population: List[Individual]):
    return len(population) < 11


def simulate():
    individuals = 100
    survivor_percentage = .49
    child_ratio = 2
    no_of_matches = None

    population = []
    matches, markets = data_transformation.get_matches_and_markets()
    matches = data_transformation.merge_matches_with_markets(matches, markets)

    if no_of_matches is not None:
        matches = matches[:no_of_matches]

    for _ in range(individuals):
        individual = generate_new_individual()
        population.append(individual)

    while True:
        population = reset_population_states(population)
        population = betting.bet_matches(population, matches)

        print(f"{Fore.BLUE}============================={Style.RESET_ALL}")
        print('population size', len(population))
        print('median cash:', statistics.median([individual.cash for individual in population]))
        print('highest cash:', max(individual.cash for individual in population))
        print('lowest cash:', min(individual.cash for individual in population))
        print(f"{Fore.BLUE}============================={Style.RESET_ALL}")

        population = selection(population, survivor_percentage)

        if end_condition(population):
            break

        population = generate_children(population, child_ratio)

    for individual in population:
        print(f'{Fore.GREEN}\nINDIVIDUAL\ncash: {individual.cash}\nbets: {individual.placed_bets_number} \nstrategies:{Style.RESET_ALL}')
        for strategy in individual.strategies:
            if strategy.action == Action.BUY:
                print('Buy when:')
            if strategy.action == Action.SETTLE:
                print('Settle when:')
            for params in strategy.parameters:
                print(f'- {params.name.value} is {params.comparison.value}: {params.value} placing {params.money_share} percent of cash')
