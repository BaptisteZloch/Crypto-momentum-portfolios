from __future__ import annotations
from typing import Optional, Self, Union
import pandas as pd


class Indicators:
    """
    Indicators is a singleton utility class for computing some financial indicators on crypto data.

    Protected Attributes:
    ----
        _instance (Optional[Indicators]): The singleton instance of Indicators.

    Methods:
    ----
        momentum(crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24) -> Union[pd.Series, pd.DataFrame]:
            Compute the momentum of a crypto asset over a given lookback period.
        volatility(crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24) -> Union[pd.Series, pd.DataFrame]:
            Compute the realized volatility of a crypto asset over a given lookback period.
        instantaneous_volatility(crypto_data: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
            Compute the instantaneous volatility of a crypto asset.
        __new__() -> Self:
            Create a singleton instance of the Indicators class.
    """

    _instance: Optional[Indicators] = None

    @staticmethod
    def momentum(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24
    ) -> Union[pd.Series, pd.DataFrame]:
        """Compute the momentum of a crypto asset over a given lookback period.

        Args:
        ----
            crypto_data (Union[pd.Series, pd.DataFrame]): The data to compute the momentum on.
            lookback (int, optional): The momentum calculation window. Defaults to 24.

        Returns:
        ----
            Union[pd.Series, pd.DataFrame]: The momentum of the crypto.
        """
        return crypto_data.rolling(lookback).apply(lambda x: x[-1] / x[0]).fillna(1)

    @staticmethod
    def volatility(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24
    ) -> Union[pd.Series, pd.DataFrame]:
        """Compute the realized volatility of a crypto asset over a given lookback period.

        Args:
        ----
            crypto_data (Union[pd.Series, pd.DataFrame]): The data to compute the historical volatility on.
            lookback (int, optional): The volatility calculation window. Defaults to 24.

        Returns:
        ----
            Union[pd.Series, pd.DataFrame]: The historical volatility of the crypto.
        """
        return crypto_data.rolling(lookback).std()

    @staticmethod
    def instantaneous_volatility(
        crypto_data: Union[pd.Series, pd.DataFrame]
    ) -> Union[pd.Series, pd.DataFrame]:
        """Compute the instantaneous volatility of a crypto asset.

        Args:
            crypto_data (Union[pd.Series, pd.DataFrame]): The data to compute the instantaneous volatility on.

        Returns:
            Union[pd.Series, pd.DataFrame]: The instantaneous volatility of the crypto.
        """
        return crypto_data.pct_change().fillna(0) ** 2

    def __new__(cls) -> Self:
        """Create a singleton instance of the Indicators class.

        Returns:
            Self: The singleton instance of the Indicators class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
