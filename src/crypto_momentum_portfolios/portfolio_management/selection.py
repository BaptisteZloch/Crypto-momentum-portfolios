from typing import Union

import pandas as pd


def rank_by_field(universe: Union[pd.DataFrame, pd.Series], field: str):
    return universe[f"{field}"].iloc[-1].sort_values(ascending=False).index.to_list()


def rank_by_field_for_rows(row: Union[pd.DataFrame, pd.Series], field: str):
    return row[f"{field}"].sort_values(ascending=False).index.to_list()
