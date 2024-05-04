from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

from models.market import MarketKeys
from models.match import MatchKeys
from utils import data_transformation


@dataclass
class Prediction:
    time: int
    prediction: float


def run_model_test():
    print('\n-- ARIMA (temporarily) --')

    market_index = 3
    minute_pred = 1

    predictions = pd.DataFrame()

    matches, markets = data_transformation.get_matches_and_markets()
    markets_list = data_transformation.merge_matches_with_markets(matches, markets)

    test_match = markets_list[1]

    for i, _ in test_match.iterrows():
        if i < 2:
            continue

        train_data: pd.DataFrame = test_match.iloc[:i]
        train_series: pd.Series = train_data[MarketKeys.home_back_1_price.value].squeeze()

        model = ARIMA(train_series, order=(1, 0, 0))
        model_fit = model.fit()

        forecast = model_fit.forecast(steps=1)

        prediction = {
            'time': train_data.iloc[-1][MarketKeys.minutes_to_match.value] - 1,
            'odds': round(forecast, 2)
        }
        predictions = predictions.append(prediction, ignore_index=True)

    actual_odds = pd.DataFrame()
    actual_odds = actual_odds.assign(time=test_match.pop(MarketKeys.minutes_to_match.value))
    actual_odds = actual_odds.assign(odds=test_match.pop(MarketKeys.home_back_1_price))
    actual_odds = actual_odds.drop(index=[0, 1, 2])

    predictions = predictions.tail(-1)
    predictions['odds'] = predictions['odds'].astype(float)

    plt.plot(actual_odds['odds'], label='Values')
    plt.plot(predictions['odds'], label='Predictions')

    x_labels = actual_odds['time'].tolist()
    x_positions = np.arange(len(x_labels))

    step = 5

    x_positions_spaced = x_positions[::step]
    x_labels_spaced = x_labels[::step]

    plt.xticks(x_positions_spaced, x_labels_spaced, rotation=45, ha='right')

    plt.legend()
    plt.xlabel('Index')
    plt.ylabel('Y')

    plt.show()

    total_rows = len(actual_odds)
    matching_count = 0
    for value1, value2 in zip(actual_odds['odds'], predictions['odds']):
        if value1 == value2:
            matching_count += 1

    matching_percentage = (matching_count / total_rows) * 100

    for i, _ in actual_odds.iterrows():
        print(f'ACTUAL: {actual_odds.iloc[i]["odds"]} PREDICTED: {predictions.iloc[i]["odds"]}')

    print(matching_percentage)


def run_model():
    print('\n-- ARIMAX --')

    accuracies = []
    rmses = []

    matches, markets = data_transformation.get_matches_and_markets()
    markets_list = data_transformation.merge_matches_with_markets(matches, markets)

    for i, market in enumerate(markets_list):
        market = data_transformation.fill_empty_values(market)

        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

        market[MarketKeys.last_match_time.value] = data_transformation.date_to_number(
            market[MarketKeys.last_match_time.value],
            date_format
        )
        market[MatchKeys.open_date.value] = data_transformation.date_to_number(
            market[MatchKeys.open_date.value],
            date_format
        )

        teams_categories = data_transformation.create_categories(
            market[[MatchKeys.home_team.value, MatchKeys.away_team.value]]
        )

        market[MatchKeys.home_team.value] = data_transformation.category_to_number(
            market[MatchKeys.home_team.value],
            teams_categories
        )
        market[MatchKeys.away_team.value] = data_transformation.category_to_number(
            market[MatchKeys.away_team.value],
            teams_categories
        )
        market[MatchKeys.country_code.value] = data_transformation.category_to_number(
            market[MatchKeys.country_code.value]
        )

        market[MatchKeys.market_id.value] = data_transformation.object_to_number(market[MatchKeys.market_id.value])

        time_series_data = market[MarketKeys.home_back_1_price.value]
        time_series_data = time_series_data.to_numpy()

        exogenous_data = market.drop(MarketKeys.home_back_1_price.value, axis=1)
        exogenous_data = data_transformation.remove_constant_columns(exogenous_data)

        time_series_train, time_series_test = data_transformation.split_train_and_test(time_series_data)
        exogenous_data_train, exogenous_data_test = data_transformation.split_train_and_test(exogenous_data)

        model = ARIMA(time_series_train, exog=exogenous_data_train, order=(1, 0, 0))
        model_fit = model.fit()

        predictions = model_fit.forecast(steps=len(time_series_test), exog=exogenous_data_test)

        accuracy = (1 - np.mean(np.abs((time_series_test - predictions) / time_series_test)))
        accuracies.append(accuracy)

        rmse = np.sqrt(mean_squared_error(time_series_test, predictions))
        rmses.append(rmse)

    avg_accuracy = sum(accuracies) / len(accuracies)
    avg_rmse = sum(rmses) / len(rmses)

    print("Average accuracy:", avg_accuracy)
    print("Average RMSE:", avg_rmse)
