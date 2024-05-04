import pandas as pd

import config.competitions
import config.market_start
from config.other import limit
from data_gathering import data_download, data_segregation
from models.market import Market, MarketKeys
from models.match import Match, MatchKeys
from utils import data_transformation
from data_gathering.data_collection import get_time_range
from utils import file_operations
from config import paths


def download_events():
    competition_ids = [competition.ID for competition in config.competitions.Competitions]
    start_time_str, end_time_str = get_time_range()
    data_download.download_events(competition_ids, limit, start_time_str, end_time_str)


def print_events():
    data_segregation.get_formatted_events(True)


def download_markets():
    events = data_segregation.get_formatted_events()
    market_ids = events['marketId'].values
    data_download.download_markets(market_ids, limit)


def print_markets():
    data_segregation.get_formatted_matches(True)


def print_odds(market_id):
    data_segregation.get_formatted_market_odds(market_id, True)


def print_csv(filename: str):
    pd.set_option("display.precision", 15)
    data = pd.read_csv(f"{paths.main_path}/data/{filename}.csv")
    file_operations.save_table(data)


def convert_to_new_models():
    matches: pd.DataFrame
    matches, markets_list = data_transformation.get_matches_and_markets()

    for i, market in enumerate(markets_list):
        try:
            value = market[MarketKeys.home_back_1_price.value]
        except Exception as e:
            new_columns = {
                'minutesToMatch': MarketKeys.minutes_to_match.value,
                'lastMatchTime': MarketKeys.last_match_time.value,
                'totalMatched': MarketKeys.total_matched.value,
                'totalAvailable': MarketKeys.total_available.value,
                'homeLastPriceTraded': MarketKeys.home_last_price_traded.value,
                'awayLastPriceTraded': MarketKeys.away_last_price_traded.value,
                'drawLastPriceTraded': MarketKeys.draw_last_price_traded.value,
                'homeBack1Price': MarketKeys.home_back_1_price.value,
                'homeBack2Price': MarketKeys.home_back_2_price.value,
                'homeBack3Price': MarketKeys.home_back_3_price.value,
                'awayBack1Price': MarketKeys.away_back_1_price.value,
                'awayBack2Price': MarketKeys.away_back_2_price.value,
                'awayBack3Price': MarketKeys.away_back_3_price.value,
                'drawBack1Price': MarketKeys.draw_back_1_price.value,
                'drawBack2Price': MarketKeys.draw_back_2_price.value,
                'drawBack3Price': MarketKeys.draw_back_3_price.value,
                'homeBack1Size': MarketKeys.home_back_1_size.value,
                'homeBack2Size': MarketKeys.home_back_2_size.value,
                'homeBack3Size': MarketKeys.home_back_3_size.value,
                'awayBack1Size': MarketKeys.away_back_1_size.value,
                'awayBack2Size': MarketKeys.away_back_2_size.value,
                'awayBack3Size': MarketKeys.away_back_3_size.value,
                'drawBack1Size': MarketKeys.draw_back_1_size.value,
                'drawBack2Size': MarketKeys.draw_back_2_size.value,
                'drawBack3Size': MarketKeys.draw_back_3_size.value,
                'homeLay1Price': MarketKeys.home_lay_1_price.value,
                'homeLay2Price': MarketKeys.home_lay_2_price.value,
                'homeLay3Price': MarketKeys.home_lay_3_price.value,
                'awayLay1Price': MarketKeys.away_lay_1_price.value,
                'awayLay2Price': MarketKeys.away_lay_2_price.value,
                'awayLay3Price': MarketKeys.away_lay_3_price.value,
                'drawLay1Price': MarketKeys.draw_lay_1_price.value,
                'drawLay2Price': MarketKeys.draw_lay_2_price.value,
                'drawLay3Price': MarketKeys.draw_lay_3_price.value,
                'homeLay1Size': MarketKeys.home_lay_1_size.value,
                'homeLay2Size': MarketKeys.home_lay_2_size.value,
                'homeLay3Size': MarketKeys.home_lay_3_size.value,
                'awayLay1Size': MarketKeys.away_lay_1_size.value,
                'awayLay2Size': MarketKeys.away_lay_2_size.value,
                'awayLay3Size': MarketKeys.away_lay_3_size.value,
                'drawLay1Size': MarketKeys.draw_lay_1_size.value,
                'drawLay2Size': MarketKeys.draw_lay_2_size.value,
                'drawLay3Size': MarketKeys.draw_lay_3_size.value,
            }

            columns_to_remove = ['homeTotalMatched', 'awayTotalMatched', 'drawTotalMatched']

            market: pd.DataFrame
            market = market.rename(columns=new_columns)
            market = market.drop(columns=columns_to_remove)

            market_id = matches.at[i, MatchKeys.market_id.value]

            print(f'Old columns in market: {market_id}')

            file_operations.overwrite_csv(market, f'{paths.main_path}/data/{market_id}.csv')


def delete_on_condition():
    matches: pd.DataFrame
    matches, markets_list = data_transformation.get_matches_and_markets()
    markets_list = data_transformation.merge_matches_with_markets(matches, markets_list)

    for i, market in enumerate(markets_list):
        column = market[Market.home_back_1_price]
        all_values_same = all(value == column.iloc[0] for value in column)

        if all_values_same:
            market_id = market[Match.market_id][0]
            file_operations.remove_market_file(f'{paths.main_path}/data/{market_id}.csv')
            matches.drop(inplace=True, index=i)
            file_operations.overwrite_csv(matches, f'{paths.main_path}/data/matches.csv')


def print_dataframe(df: pd.DataFrame):
    file_operations.save_table(df)

