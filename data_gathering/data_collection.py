import datetime
from time import sleep
from typing import List

import pandas as pd

from config.competitions import Competitions
from config.leagues import Leagues
from config.market_start import start_hour, start_minute, end_hour, end_minute
from data_gathering import data_segregation, data_download
from models.market import MarketKeys
from utils import file_operations
from config import paths

limit = 100


def get_time_range() -> (str, str):
    now = datetime.datetime.utcnow()
    start_time = now + datetime.timedelta(hours=start_hour)
    start_time = start_time.replace(minute=start_minute, second=0, microsecond=0)
    end_time = now + datetime.timedelta(hours=end_hour)
    end_time = end_time.replace(minute=end_minute, second=0, microsecond=0)
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return start_time_str, end_time_str


def get_events(start_time_str: str, end_time_str: str) -> pd.DataFrame:
    competition_ids = [competition.ID for competition in Competitions]
    data_download.download_events(competition_ids, limit, start_time_str, end_time_str)
    events = data_segregation.get_formatted_events()
    if events.empty:
        return events
    league_ids = [league.ID for league in Leagues]
    events = events[events['competitionId'].isin(league_ids)]
    return events


def get_markets(market_ids: List[str]) -> pd.DataFrame:
    data_download.download_markets(market_ids, limit)
    markets = data_segregation.get_formatted_matches()
    return markets


def remove_closed_markets(market_ids: List[str], infinite=False) -> List[str]:
    new_market_ids = []
    for market_id in market_ids:
        market_odds = data_segregation.get_formatted_market_odds(market_id)
        if market_odds[MarketKeys.minutes_to_match.value].values[0] < 0:
            print(f"Market {market_id} is closed.")
            if infinite:
                file_operations.append_txt_file(
                    f"{datetime.datetime.now()}: Market {market_id} is closed.",
                    paths.logs_filepath
                )
        else:
            new_market_ids.append(market_id)
    return new_market_ids


def collect_data(infinite=False):
    try:
        if infinite:
            file_operations.append_txt_file(f'~~~ Started ~~~', paths.logs_filepath)
        while True:
            start_time_str, end_time_str = get_time_range()
            events = get_events(start_time_str, end_time_str)
            if events.empty:
                if infinite:
                    sleep(60)
                    continue
                else:
                    break
            market_ids = events['marketId'].values
            markets = get_markets(market_ids)
            file_operations.append_csv(markets, f'{paths.main_path}/data/matches.csv')
            while True:
                get_markets(market_ids)
                market_ids = remove_closed_markets(market_ids, infinite)
                if not market_ids:
                    print("All markets are closed.")
                    if infinite:
                        file_operations.append_txt_file(
                            f"{datetime.datetime.now()}: All markets are closed.",
                            paths.logs_filepath
                        )
                    break
                for market_id in market_ids:
                    market_odds = data_segregation.get_formatted_market_odds(market_id)
                    file_operations.append_csv(market_odds, f"{paths.main_path}/data/{str(market_id)}.csv")
                sleep(60)
            if infinite is False:
                break
            sleep(60)
    except Exception as e:
        print(e)

        if infinite:
            file_operations.append_txt_file(f'\n==========\n{e}\n==========\n', paths.logs_filepath)
            collect_data(infinite)

