from datetime import datetime

import pandas as pd

from config.paths import events_filename, markets_filename
from models.market import Market, MarketKeys
from models.match import Match
from utils import file_operations

pd.set_option('display.max_columns', None)


def get_formatted_events(print_table=False) -> pd.DataFrame:
    data = file_operations.load_json(events_filename)
    attachments = data['attachments']
    if 'competitions' not in attachments:
        if print_table:
            print('No data in events.json')
        return pd.DataFrame()
    competitions = data['attachments']['competitions']
    events = list(data['results'])
    for event in events:
        competition_id = str(event['competitionId'])
        event['competitionName'] = competitions[competition_id]['name']
    data = pd.DataFrame(list(events))
    if print_table:
        file_operations.save_table(data)
    return data


def get_flattened_match_data(market: pd.DataFrame) -> Match:
    node = market['marketNodes'][0]
    home, away = node['runners'][:2]

    return Match(
        market['eventId'],
        node['marketId'],
        market['event']['openDate'],
        home['description']['runnerName'],
        away['description']['runnerName'],
        market['event']['countryCode'] if 'countryCode' in market['event'] else None,
    )


def get_flattened_market_odds(market) -> Market:
    runners = {
        'home': market['marketNodes'][0]['runners'][0],
        'away': market['marketNodes'][0]['runners'][1],
        'draw': market['marketNodes'][0]['runners'][2],
    }

    # calculate minutes to match
    open_date_str = market['event']['openDate']
    open_date = datetime.fromisoformat(open_date_str[:-1])  # remove 'Z' at the end
    minutes_to_match = int((open_date - datetime.utcnow()).total_seconds() / 60)

    result = {
        MarketKeys.minutes_to_match.value: minutes_to_match,
        MarketKeys.last_match_time.value: market['marketNodes'][0]['state']['lastMatchTime'],
        MarketKeys.total_matched.value: market['marketNodes'][0]['state']['totalMatched'],
        MarketKeys.total_available.value: market['marketNodes'][0]['state']['totalAvailable'],
    }

    for runner_name, runner in runners.items():
        result[f'{runner_name}_last_price_traded'] = runner['state']['lastPriceTraded']

        for i in range(3):
            for side in ['back', 'lay']:
                for j, price_size in enumerate(runner['exchange'][f'availableTo{side.capitalize()}']):
                    if j == i:
                        result[f'{runner_name}_{side}_{i + 1}_price'] = price_size.get('price')
                        result[f'{runner_name}_{side}_{i + 1}_size'] = price_size.get('size')
                        break
                else:
                    result[f'{runner_name}_{side}_{i + 1}_price'] = None
                    result[f'{runner_name}_{side}_{i + 1}_size'] = None

    return Market(**result)


def get_formatted_matches(print_table=False) -> pd.DataFrame:
    data = file_operations.load_json(markets_filename)
    markets = data['eventTypes'][0]['eventNodes']
    markets = map(lambda market: get_flattened_match_data(market), markets)
    data = pd.DataFrame(list(markets))
    if print_table:
        file_operations.save_table(data)
    return data


def get_formatted_market_odds(market_id, print_table=False) -> pd.DataFrame:
    data = file_operations.load_json(markets_filename)
    markets = data['eventTypes'][0]['eventNodes']
    markets = filter(lambda market: market['marketNodes'][0]['marketId'] == market_id, markets)
    markets = map(lambda market: get_flattened_market_odds(market), markets)
    data = pd.DataFrame(list(markets))
    if print_table:
        file_operations.save_table(data)
    return data
