from typing import List, Dict

import numpy as np
import pandas as pd

from models.market import MarketKeys
from models.match import MatchKeys
from config import paths


def date_to_number(series: pd.Series, date_format: str) -> pd.Series:
    converted_series = pd.to_datetime(series, format=date_format)
    converted_series = converted_series.astype(np.int64)
    return converted_series


def create_categories(columns: pd.DataFrame) -> Dict[str, int]:
    combined_values = pd.Series(columns.values.flatten())
    categories, _ = pd.factorize(combined_values)
    categories_dict = {value: label for value, label in zip(combined_values, categories)}
    return categories_dict


def category_to_number(series: pd.Series, categories: Dict[str, int] = None) -> pd.Series:
    if categories is None:
        categories = create_categories(pd.DataFrame(series))
    return series.map(categories)


def object_to_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors='coerce')


def merge_matches_with_markets(matches: pd.DataFrame, markets: List[pd.DataFrame]) -> List[pd.DataFrame]:
    merged_markets = []
    for i, market in enumerate(markets):
        merged_market = market.assign(**matches.iloc[i])
        merged_markets.append(merged_market)
    return merged_markets


def get_matches_and_markets() -> (pd.DataFrame, List[pd.DataFrame]):
    matches = pd.read_csv(f'{paths.main_path}/data/matches.csv', dtype={MatchKeys.market_id.value: str})
    markets = []
    for i, match in matches.iterrows():
        markets.append(pd.read_csv(f'{paths.main_path}/data/{match[MatchKeys.market_id.value]}.csv'))
    return matches, markets


def merge_markets(markets: List[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(markets, ignore_index=True)


def create_target_column(markets: pd.DataFrame) -> pd.DataFrame:
    markets['target'] = markets[MarketKeys.home_back_1_price.value].shift(-1)
    return markets


def fill_empty_values(markets: pd.DataFrame) -> pd.DataFrame:
    return markets.fillna(0)


def remove_constant_columns(columns: pd.DataFrame, with_log: bool = False) -> pd.DataFrame:
    exogenous_columns = columns.loc[:, (columns != columns.iloc[0]).any()]
    if with_log is True:
        dropped_columns = list(set(columns) - set(exogenous_columns.columns))
        print("Dropped columns:", dropped_columns)
        print("Remaining columns:", exogenous_columns.columns)
    return exogenous_columns


def split_train_and_test(markets: pd.DataFrame, ratio: float = 0.8) -> (List[pd.DataFrame], List[pd.DataFrame]):
    num_samples = len(markets)
    num_train_samples = int(num_samples * ratio)

    train_data = markets[:num_train_samples]
    test_data = markets[num_train_samples:]

    return train_data, test_data
