from __future__ import annotations
from typing import Any, Callable, Optional, Self, Union
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
        return (
            crypto_data.rolling(kwargs.get("momentum_lookback", lookback)).apply(
                lambda x: x[-1] / x[0]
            )
            # .fillna(1)
        )

    @staticmethod
    def volatility(
        crypto_data: Union[pd.Series, pd.DataFrame], lookback: int = 24, **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.rolling(kwargs.get("volatility_lookback", lookback)).std()

    @staticmethod
    def instantaneous_volatility(
        crypto_data: Union[pd.Series, pd.DataFrame], **kwargs
    ) -> Union[pd.Series, pd.DataFrame]:
        return crypto_data.pct_change() ** 2  # .fillna(0)

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


INDICATOR_MAPPING: dict[
    str,
    Callable[
        [
            Union[pd.DataFrame, pd.Series],
        ],
        Union[pd.DataFrame, pd.Series],
    ],
] = {   
    "returns": Indicators.returns,
    "momentum": Indicators.momentum,
    "volatility": Indicators.volatility,
    "instantaneous_volatility": Indicators.instantaneous_volatility,
    "long_ema": Indicators.long_ema,
    "short_ema": Indicators.short_ema,
    "short_ma": Indicators.short_ma,
    "long_ma": Indicators.long_ma,
}


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
