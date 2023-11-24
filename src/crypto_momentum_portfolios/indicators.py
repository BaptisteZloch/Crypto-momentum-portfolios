from __future__ import annotations
from typing import Optional, Self, Union
import pandas as pd


class Indicators:
    _instance: Optional[Indicators] = None

    @staticmethod
    def momentum(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(lookback).apply(lambda x: x[-1] / x[0]).fillna(1)

    @staticmethod
    def volatility(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(lookback).std()

    @staticmethod
    def instantaneous_volatility(crypto_data: Union[pd.Series, pd.DataFrame]):
        return crypto_data.pct_change().fillna(0) ** 2

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
