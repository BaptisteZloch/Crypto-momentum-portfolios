import pandas as pd
from typing import Self
from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Self, Tuple

from tqdm import tqdm
from crypto_momentum_portfolios.portfolio_management.allocation import (
    capi_weighted_allocation,
    equal_weighted_allocation,
)
from crypto_momentum_portfolios.utility.constants import (
    SLIPPAGE_EFFECT,
    TRANSACTION_COST,
)
from crypto_momentum_portfolios.utility.types import Fields, Side, RebalanceFrequency
from crypto_momentum_portfolios.utility.utils import get_rebalance_dates
from crypto_momentum_portfolios.utility.types import Fields, Side, RebalanceFrequency


class BenchmarkDataFrameBuilderABC(ABC):
    _benchmarks: Optional[pd.DataFrame] = None

    @abstractmethod
    def build_capitalization_weighted_benchmark(self):
        raise NotImplementedError

    @abstractmethod
    def build_equally_weighted_benchmark(self):
        raise NotImplementedError

    def collect_benchmark_returns(self) -> pd.DataFrame:
        if self._benchmarks is None:
            raise AttributeError(
                "You must first build the benchmarks using build_capitalization_weighted_benchmark, ... functions before collecting them"
            )

        return self._benchmarks

    @staticmethod
    def _build_capitalization_weighted_benchmark(
        universe: pd.DataFrame,
        capitalization_field: Fields = Fields.MARKET_CAP,
        rebalance_frequency: RebalanceFrequency = RebalanceFrequency.MONTH_START,
        side: Side = Side.LONG,
        verbose: bool = False,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Build a capitalization weighted benchmark

        Args:
        ----
            universe (pd.DataFrame): The universe of securities i.e MultiIndex DataFrame with the price and returns of each security as the first level of columns, the cryptos names as second level and the date as the index
            capitalization_field (Fields, optional): The field to use as capitalization in the universe DataFrame. Defaults to Fields.MARKET_CAP.
            rebalance_frequency (RebalanceFrequency, optional): The portfolio/benchmark rebalance frequency. Defaults to RebalanceFrequency.MONTH_START.
            side (Side, optional): Whether building a LONG or SHORT portfolio/benchmark. Defaults to Side.LONG.
            verbose (bool, optional): Print the rebalance dates (could be used for sanity check). Defaults to False.

        Returns:
        ----
            Tuple[pd.DataFrame, pd.DataFrame]: The returns DataFrame and weights DataFrame of the capi weighted benchmark.
        """
        returns_histo, weights_histo = [], []
        REBALANCE_DATES = get_rebalance_dates(
            universe.index[0], universe.index[-1], rebalance_frequency
        )

        SECURITIES = universe["price"].columns.to_list()

        for index, row in tqdm(
            universe.iterrows(),
            desc="Building the Benchmark...",
            total=len(universe),
            leave=False,
        ):
            if index in REBALANCE_DATES or index == universe.index[0]:
                if verbose:
                    print(f"Rebalancing the portfolio on {index}")
                weights = capi_weighted_allocation(
                    SECURITIES, row[capitalization_field]
                )

            weights_histo.append(weights)
            returns = universe.loc[index, "returns"][SECURITIES].to_numpy()

            weights_np = np.array(list(weights.values()))
            if index in REBALANCE_DATES or index == universe.index[0]:
                returns_histo.append(
                    (
                        (returns @ weights_np)
                        - TRANSACTION_COST * len(SECURITIES)
                        - SLIPPAGE_EFFECT
                    )
                    * side
                )
            else:
                returns_histo.append((returns @ weights_np) * side)
            new_weights = {
                security: unit_weight
                for security, unit_weight in zip(
                    SECURITIES,
                    (weights_np * (returns + 1)) / ((returns + 1) @ weights_np),
                )
            }
            weights = new_weights

        return pd.DataFrame(
            returns_histo,
            columns=["capi_weighted_benchmark"],
            index=universe.index,
            dtype=float,
        ), pd.DataFrame(weights_histo, index=universe.index, dtype=float).fillna(0)

    @staticmethod
    def _build_equally_weighted_benchmark(
        universe: pd.DataFrame,
        rebalance_frequency: RebalanceFrequency = RebalanceFrequency.MONTH_START,
        side: Side = Side.LONG,
        verbose: bool = False,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Build an equally weighted benchmark

            Args:
            ----
                universe (pd.DataFrame): The universe of securities i.e MultiIndex DataFrame with the price and returns of each security as the first level of columns, the cryptos names as second level and the date as the index
                rebalance_frequency (RebalanceFrequency, optional): The portfolio/benchmark rebalance frequency. Defaults to RebalanceFrequency.MONTH_START.
                side (Side, optional): Whether building a LONG or SHORT portfolio/benchmark. Defaults to Side.LONG.
                verbose (bool, optional): Print the rebalance dates (could be used for sanity check). Defaults to False.

            Returns:
            ----
                Tuple[pd.DataFrame, pd.DataFrame]: The returns DataFrame and weights DataFrame of the equally weighted benchmark.

        ```python
        returns_df, weights_bench = build_capitalization_weighted_benchmark(universe,
                                                                    capitalization_field=Fields.MARKET_CAP,
                                                                    rebalance_frequency=RebalanceFrequency.MONTHLY,
                                                                    side=Side.LONG,
                                                                    verbose=False)
        ```
        """
        returns_histo, weights_histo = [], []
        REBALANCE_DATES = get_rebalance_dates(
            universe.index[0], universe.index[-1], rebalance_frequency
        )

        SECURITIES = universe["price"].columns.to_list()

        for index, row in tqdm(
            universe.iterrows(),
            desc="Building the Benchmark...",
            total=len(universe),
            leave=False,
        ):
            if index in REBALANCE_DATES or index == universe.index[0]:
                if verbose:
                    print(f"Rebalancing the portfolio on {index}")
                weights = equal_weighted_allocation(
                    SECURITIES,
                )

            weights_histo.append(weights)
            returns = universe.loc[index, "returns"][SECURITIES].to_numpy()

            weights_np = np.array(list(weights.values()))
            if index in REBALANCE_DATES or index == universe.index[0]:
                returns_histo.append(
                    (
                        (returns @ weights_np)
                        - TRANSACTION_COST * len(SECURITIES)
                        - SLIPPAGE_EFFECT
                    )
                    * side
                )
            else:
                returns_histo.append((returns @ weights_np) * side)
            new_weights = {
                security: unit_weight
                for security, unit_weight in zip(
                    SECURITIES,
                    (weights_np * (returns + 1)) / ((returns + 1) @ weights_np),
                )
            }
            weights = new_weights

        return pd.DataFrame(
            returns_histo,
            columns=["equal_weighted_benchmark"],
            index=universe.index,
            dtype=float,
        ), pd.DataFrame(weights_histo, index=universe.index, dtype=float).fillna(0)

    def _add_benchmark(self, dataframe: pd.DataFrame) -> None:
        if self._benchmarks is None:
            self._benchmarks = dataframe
        else:
            self._benchmarks = pd.concat([self._benchmarks, dataframe], axis=1)


class BenchmarkDataFrameBuilder(BenchmarkDataFrameBuilderABC):
    def __init__(self, universe: pd.DataFrame) -> None:
        self.__universe = universe

    def build_capitalization_weighted_benchmark(
        self,
        capitalization_field: Fields = Fields.MARKET_CAP,
        rebalance_frequency: RebalanceFrequency = RebalanceFrequency.MONTH_START,
        side: Side = Side.LONG,
        verbose: bool = False,
    ) -> Self:
        returns_df, _ = self._build_capitalization_weighted_benchmark(
            self.__universe, capitalization_field, rebalance_frequency, side, verbose
        )
        self._add_benchmark(returns_df)
        return self

    def build_bitcoin_benchmark(
        self,
    ) -> Self:
        self._add_benchmark(
            self.__universe["returns"]["BTC-USDT"].rename("bitcoin_benchmark")
        )
        return self

    def build_equally_weighted_benchmark(
        self,
        rebalance_frequency: RebalanceFrequency = RebalanceFrequency.MONTH_START,
        side: Side = Side.LONG,
        verbose: bool = False,
    ) -> Self:
        returns_df, _ = self._build_equally_weighted_benchmark(
            self.__universe, rebalance_frequency, side, verbose
        )
        self._add_benchmark(returns_df)

        return self
