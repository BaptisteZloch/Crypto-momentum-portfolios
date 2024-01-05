from __future__ import annotations
from typing import Any, Callable, Optional, Self, Union
import numpy as np
import pandas as pd


class Indicators:
    _instance: Optional[Self] = None

    @staticmethod
    def long_ema(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.ewm(kwargs.get("long_ema_lookback", lookback)).mean()

    @staticmethod
    def short_ema(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.ewm(kwargs.get("short_ema_lookback", lookback)).mean()

    @staticmethod
    def short_ma(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(kwargs.get("short_ma_lookback", lookback)).mean()

    @staticmethod
    def long_ma(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(kwargs.get("long_ma_lookback", lookback)).mean()

    @staticmethod
    def returns(
        crypto_data: Union[pd.Series, pd.DataFrame], **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.pct_change()  # .fillna(0)

    @staticmethod
    def momentum(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(kwargs.get("momentum_lookback", lookback)).apply(
            lambda x: (x[-1] / x[0]) - 1
        )

    @staticmethod
    def ema_momentum(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data/Indicators.long_ema(crypto_data, lookback, **kwargs)

    @staticmethod
    def ts_momentum(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 12, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        returns = Indicators.returns(crypto_data, **kwargs)
        return (
            Indicators.volatility(crypto_data, lookback, **kwargs).apply(
                lambda vol: 0.4 / vol
            )
            * returns.shift(kwargs.get("ts_momentum_lookback", lookback)).apply(np.sign)
            * returns
        )

    @staticmethod
    def volatility_neutralized_momentum(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return Indicators.momentum(
            crypto_data, kwargs.get("momentum_lookback", lookback), **kwargs
        ) / Indicators.volatility(
            crypto_data, kwargs.get("volatility_lookback", lookback), **kwargs
        )

    @staticmethod
    def volatility(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(kwargs.get("volatility_lookback", lookback)).std()

    # @staticmethod
    # def ex_ante_volatility(
    #     crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    # ) -> Union[pd.Series, pd.DataFrame]:
    #     ema_returns = Indicators.long_ema(
    #         Indicators.returns(crypto_data, **kwargs), lookback, **kwargs
    #     )
    #     delta = -1 * 60 / 59
    #     n = 365
    #     return crypto_data.rolling(kwargs.get("volatility_lookback", lookback)).std()

    @staticmethod
    def instantaneous_volatility(
        crypto_data: Union[pd.Series, pd.DataFrame], **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.pct_change() ** 2  # .fillna(0)

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# class Indicators:
#     """
#     Indicators is a singleton utility class for computing some financial indicators on crypto data.

#     Protected Attributes:
#     ----
#         _instance (Optional[Indicators]): The singleton instance of Indicators.

#     Methods:
#     ----
#         momentum(crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24) -> Union[pd.Series, pd.DataFrame]:
#             Compute the momentum of a crypto asset over a given lookback period.
#         volatility(crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24) -> Union[pd.Series, pd.DataFrame]:
#             Compute the realized volatility of a crypto asset over a given lookback period.
#         instantaneous_volatility(crypto_data: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
#             Compute the instantaneous volatility of a crypto asset.
#         __new__() -> Self:
#             Create a singleton instance of the Indicators class.
#     """

#     _instance: Optional[Indicators] = None

#     @staticmethod
#     def momentum(
#         crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24
#     ) -> Union[pd.Series, pd.DataFrame]:
#         """Compute the momentum of a crypto asset over a given lookback period.

#         Args:
#         ----
#             crypto_data (Union[pd.Series, pd.DataFrame]): The data to compute the momentum on.
#             lookback (int, optional): The momentum calculation window. Defaults to 24.

#         Returns:
#         ----
#             Union[pd.Series, pd.DataFrame]: The momentum of the crypto.
#         """
#         return crypto_data.rolling(lookback).apply(lambda x: x[-1] / x[0]).fillna(1)

#     @staticmethod
#     def volatility(
#         crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24
#     ) -> Union[pd.Series, pd.DataFrame]:
#         """Compute the realized volatility of a crypto asset over a given lookback period.

#         Args:
#         ----
#             crypto_data (Union[pd.Series, pd.DataFrame]): The data to compute the historical volatility on.
#             lookback (int, optional): The volatility calculation window. Defaults to 24.

#         Returns:
#         ----
#             Union[pd.Series, pd.DataFrame]: The historical volatility of the crypto.
#         """
#         return crypto_data.rolling(lookback).std()

#     @staticmethod
#     def instantaneous_volatility(
#         crypto_data: Union[pd.Series, pd.DataFrame]
#     ) -> Union[pd.Series, pd.DataFrame]:
#         """Compute the instantaneous volatility of a crypto asset.

#         Args:
#             crypto_data (Union[pd.Series, pd.DataFrame]): The data to compute the instantaneous volatility on.

#         Returns:
#             Union[pd.Series, pd.DataFrame]: The instantaneous volatility of the crypto.
#         """
#         return crypto_data.pct_change().fillna(0) ** 2

#     def __new__(cls) -> Self:
#         """Create a singleton instance of the Indicators class.

#         Returns:
#             Self: The singleton instance of the Indicators class.
#         """
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#         return cls._instance
