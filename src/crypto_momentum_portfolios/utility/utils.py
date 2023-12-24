from datetime import datetime
from functools import lru_cache
from typing import Tuple, Union
import pandas as pd

from crypto_momentum_portfolios.utility.types import RebalanceFrequency


@lru_cache(maxsize=32, typed=True)
def get_rebalance_dates(
    start_date: Union[datetime, str],
    end_date: Union[datetime, str],
    frequency: RebalanceFrequency = RebalanceFrequency.MONTH_START,
) -> Tuple[datetime, ...]:
    """Generate a Series of the rebalance date during the backtest period based on the frequency.

    Args:
        start_date (Union[datetime, str]): The start date.
        end_date (Union[datetime, str]):  The start date.
        frequency (RebalanceFrequency, optional): _description_. Defaults to "monthly".

    Returns:
        Tuple[datetime,...]: The rebalance dates.
    """

    return tuple(pd.date_range(start_date, end_date, freq=frequency).to_list())
