from datetime import datetime
from typing import Dict, List, Tuple, Union
import numpy as np
import numpy.typing as npt
import pandas as pd

from crypto_momentum_portfolios.utility.types import RebalanceFrequency


def get_rebalance_dates(
    start_date: Union[datetime, str],
    end_date: Union[datetime, str],
    frequency: RebalanceFrequency = RebalanceFrequency.MONTH_START,
) -> Tuple[Union[pd.Timestamp, datetime], ...]:
    """Generate a Series of the rebalance date during the backtest period based on the frequency.

    Args:
        start_date (Union[datetime, str]): The start date.
        end_date (Union[datetime, str]):  The start date.
        frequency (RebalanceFrequency, optional): _description_. Defaults to "monthly".

    Returns:
        Tuple[datetime,...]: The rebalance dates.
    """
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date, infer_datetime_format=True)
    return tuple(
        [start_date] + pd.date_range(start_date, end_date, freq=frequency).to_list()
    )


def weights_drift(
    securities: List[str],
    old_weights: npt.NDArray[np.float32],
    current_returns: npt.NDArray[np.float32],
) -> Dict[str, float]:
    """Take the old weights and the current returns and return the new weights (impacted with the drift)

    Args:
        securities (List[str]): The list of securities.
        old_weights (npt.NDArray[np.float32]): The old weights associated with the securities.
        current_returns (npt.NDArray[np.float32]): The current returns associated with the securities.

    Returns:
        Dict[str, float]: The new weights in a dict format: key=security, value=new weight.
    """
    return {
        security: unit_weight
        for security, unit_weight in zip(
            securities,
            (old_weights * (current_returns + 1))
            / ((current_returns + 1) @ old_weights),
        )
    }
