import json
import os
import webbrowser
from typing import Any
from config import paths

import pandas as pd


def append_txt_file(data: str, filename: str):
    with open(filename, 'a') as file:
        file.write(f'{data}\n')


def save_json(filename: str, json_data: Any):
    with open(f'{paths.main_path}/tmp_data/{filename}.json', 'w') as outfile:
        outfile.write(json_data)


def load_json(filename: str) -> Any:
    with open(f'{paths.main_path}/tmp_data/{filename}.json') as json_file:
        return json.load(json_file)


def append_csv(df: pd.DataFrame, file_name: str):
    """
    Save pandas dataframe to CSV file.
    If file with the same name already exists, append new rows.
    """
    if os.path.isfile(file_name):
        df.to_csv(file_name, mode='a', header=False, index=False)
    else:
        df.to_csv(file_name, index=False)


def overwrite_csv(df: pd.DataFrame, file_name: str):
    df.to_csv(file_name, index=False)


def save_table(df: pd.DataFrame):
    def convert_float(val):
        if isinstance(val, float):
            return '{:.9f}'.format(val)
        else:
            return str(val)

    df = df.applymap(convert_float)

    table_styles = [
        {'selector': 'table', 'props': [('border-collapse', 'collapse')]},
        {'selector': 'th, td', 'props': [('border', '1px solid #ddd')]},
        {'selector': 'th',
         'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold'), ('position', 'sticky'),
                   ('top', '0'), ('box-shadow', '0 2px 2px -1px rgba(0, 0, 0, 0.4)')]},
        {'selector': 'td', 'props': [('padding', '8px'), ('text-align', 'left')]},
        {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
        {'selector': 'tr:hover', 'props': [('background-color', '#DDDDDD')]}
    ]

    styled_df = df.style.set_table_styles(table_styles)
    html = styled_df.to_html()

    filename = f'{paths.main_path}/tmp_data/table.html'
    with open(filename, 'w') as f:
        f.write(html)
    webbrowser.open(filename)


def remove_market_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} removed successfully.")
    else:
        print(f"File {file_path} does not exist.")
