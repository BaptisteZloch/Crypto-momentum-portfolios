from typing import Optional, Self, Unpack
import numpy as np
import pandas as pd
from tqdm import tqdm
from quant_invest_lab.reports import (
    plot_from_trade_df_and_ptf_optimization,
)
from crypto_momentum_portfolios.portfolio_management.allocation import (
    AllocationMethod,
    ALLOCATION_TO_FUNCTION,
    ALLOCATION_FIELDS,
)
from crypto_momentum_portfolios.portfolio_management.benchmarks import (
    BenchmarkDataFrameBuilder,
)
from crypto_momentum_portfolios.portfolio_management.performance import (
    print_performance_statistics,
)
from crypto_momentum_portfolios.portfolio_management.selection import (
    rank_by_field_for_rows,
)
from crypto_momentum_portfolios.utility.constants import (
    SLIPPAGE_EFFECT,
    TRANSACTION_COST,
)
from crypto_momentum_portfolios.utility.types import (
    AllocationMode,
    Benchmark,
    Fields,
    RankingMethod,
    RebalanceFrequency,
    RunStrategyKwargs,
    Side,
    RankingMode,
)
from crypto_momentum_portfolios.utility.utils import get_rebalance_dates, weights_drift


class PortfolioBacktester:
    _instance: Optional[Self] = None

    def __init__(
        self, universe: pd.DataFrame, benchmarks: Optional[pd.DataFrame] = None
    ) -> None:
        """Constructor method.

        Args:
            universe (pd.DataFrame): The universe of assets to backtest the strategy on with the fields.
            benchmarks (Optional[pd.DataFrame], optional): An optional dataFrame containing the 3 benchmarks ['equal_weighted_benchmark','capi_weighted_benchmark','bitcoin_benchmark']. Defaults to None.
        """
        self.__universe = universe
        if benchmarks is not None and set(Benchmark.list_values()).issubset(
            benchmarks.columns
        ):
            self.__benchmarks = benchmarks
        else:
            self.__benchmarks = (
                BenchmarkDataFrameBuilder(self.__universe)
                .build_equally_weighted_benchmark(
                    rebalance_frequency=RebalanceFrequency.MONTHLY,
                    side=Side.LONG,
                    verbose=False,
                )
                .build_capitalization_weighted_benchmark(
                    capitalization_field=Fields.MARKET_CAP,
                    rebalance_frequency=RebalanceFrequency.MONTHLY,
                    side=Side.LONG,
                    verbose=False,
                )
                .build_bitcoin_benchmark()
                .collect_benchmark_returns()
            )

    def run_strategy(
        self,
        # Selection section
        ranking_method: RankingMethod = RankingMethod.EMA_MOMENTUM,
        ranking_mode: RankingMode = RankingMode.DESCENDING,
        select_top_k_assets: int = 5,
        # Allocation section
        allocation_method: AllocationMethod = AllocationMethod.EQUAL_WEIGHTED,
        allocation_mode: AllocationMode = AllocationMode.CLASSIC,
        # Others
        rebalance_frequency: RebalanceFrequency = RebalanceFrequency.MONTHLY,
        side: Side = Side.LONG,
        benchmark: Benchmark = Benchmark.EQUAL_WEIGHTED,
        verbose: bool = False,
        print_stats: bool = True,
        plot_curve: bool = True,
        perform_t_stats: bool = True,
        **kwargs: RunStrategyKwargs,
    ):
        """Run the strategy on the universe of assets.

        Args:
        -----
            ranking_method (RankingMethod, optional): The selection method used to rank the securities in the portfolio. Defaults to RankingMethod.MOMENTUM.
            ranking_mode (RankingMode, optional): The ranking way ascending or descending order. Defaults to RankingMode.DESCENDING.
            select_top_k_assets (int, optional): The number of assets to select in the portfolio based on the ranking selection. Defaults to 5.
            allocation_method (AllocationMethod, optional): The allocation method used to allocate the weights on the selected securities. Defaults to AllocationMethod.EQUAL_WEIGHTED.
            allocation_mode (AllocationMode, optional): The allocation way classic or inverse, eg : If you allocate by volatility you better want to allocate a lower weight to the most volatile then you will use AllocationMode.INVERSE. Defaults to AllocationMode.CLASSIC.
            rebalance_frequency (RebalanceFrequency, optional): The rebalance period for the portfolio. Defaults to RebalanceFrequency.MONTHLY.
            side (Side, optional): The long or short side. Defaults to Side.LONG.
            benchmark (Benchmark, optional): The benchmark to be used for the performance statistics. Defaults to Benchmark.EQUAL_WEIGHTED.
            verbose (bool, optional): Print the rebalance dates. Defaults to False.
            print_stats (bool, optional): Print the performances and metrics of the strategy. Defaults to True.
            plot_curve (bool, optional): Plot the performance curves. Defaults to True.

        Returns:
        -----
            tuple[Series[float], DataFrame]: A tuple containing a pandas series of the returns of a dataframe of the weights of the portfolio.
        """
        assert (
            select_top_k_assets <= self.__universe["returns"].shape[1]
        ), f"select_top_k_assets must be less than or equal to {self.__universe['returns'].shape[1]}"

        returns_histo, weights_histo = [], []
        REBALANCE_DATES = get_rebalance_dates(
            start_date=self.__universe.index[0],
            end_date=self.__universe.index[-1],
            frequency=rebalance_frequency,
        )

        for index, row in tqdm(
            self.__universe.iterrows(),
            desc="Backtesting the strategy...",
            total=self.__universe.shape[0],
            leave=False,
        ):
            if index in REBALANCE_DATES and REBALANCE_DATES.index(index) == 0:
                if verbose:
                    print(f"Rebalancing the portfolio on {index}...")
                # Rank the securities in the portfolio and select the top k performing ones
                securities = rank_by_field_for_rows(
                    row=row, field=ranking_method, ascending=bool(ranking_mode)
                )[:select_top_k_assets]
                # Run allocation method on the securities
                weights = ALLOCATION_TO_FUNCTION[allocation_method](
                    securities,
                    self.__universe[ALLOCATION_FIELDS[allocation_method]][
                        securities
                    ].loc[
                        :index
                    ],  # type: ignore
                    bool(allocation_mode),
                )
            elif index in REBALANCE_DATES and REBALANCE_DATES.index(index) > 0:
                if verbose:
                    print(f"Rebalancing the portfolio on {index}...")
                # Rank the securities in the portfolio and select the top k performing ones
                securities = rank_by_field_for_rows(
                    row=row, field=ranking_method, ascending=bool(ranking_mode)
                )[:select_top_k_assets]
                # Run allocation method on the securities
                weights = ALLOCATION_TO_FUNCTION[allocation_method](
                    securities,
                    # self.__universe["returns"][securities].loc...
                    self.__universe[ALLOCATION_FIELDS[allocation_method]][
                        securities
                    ].loc[
                        REBALANCE_DATES[REBALANCE_DATES.index(index) - 1] : index
                    ],  # type: ignore
                )

            weights_histo.append(weights)  # add weights dict to the weights_histo list

            # returns is a numpy array of the returns of the securities in the portfolio
            returns = row["returns"][securities].to_numpy()
            # convert the weights dict to a numpy array
            weights_np = np.array(list(weights.values()))

            if index in REBALANCE_DATES:
                # transaction x the number of assets in the portfolio x 2 : because we buy and sell the whole portfolio
                returns_histo.append(
                    (
                        (returns @ weights_np)
                        - (
                            kwargs.get("transaction_cost", TRANSACTION_COST)
                            * select_top_k_assets
                            * 2
                        )
                        - kwargs.get("slippage_effect", SLIPPAGE_EFFECT)
                    )
                    * side
                )

            else:
                returns_histo.append((returns @ weights_np) * side)

            weights = weights_drift(securities, weights_np, returns)
        # The returns are the returns of the portfolio
        returns = pd.Series(returns_histo, index=self.__universe.index, dtype=float)
        # The weights are the weights of the portfolio
        weights_df = pd.DataFrame(
            weights_histo, index=self.__universe.index, dtype=float
        ).fillna(0)
        stats_ptf_df = []
        if print_stats:
            stats_ptf_df = print_performance_statistics(
                returns,
                self.__benchmarks[benchmark],
                perform_t_stats=perform_t_stats,
                n_samples=kwargs.get("n_bootstrap_samples", 100),
                sample_size=kwargs.get("sample_size", returns.shape[0] // 6),
                alpha_risk=kwargs.get("alpha_risk", 0.05),
            )
        if plot_curve:
            alloc = pd.DataFrame(weights_df.mean())
            alloc.columns = [0]
            alloc = alloc.T

            plot_from_trade_df_and_ptf_optimization(
                portfolio_returns=returns,
                benchmark_returns=self.__benchmarks[benchmark],
                asset_allocation_dataframe=alloc,
            )

        return returns, weights_df, stats_ptf_df

    def __new__(cls, *args, **kwargs) -> Self:
        """Singleton pattern implementation.

        Returns:
            Self: The unique instance of the class.
        """
        if cls._instance is None:
            cls._instance = super(PortfolioBacktester, cls).__new__(cls)
        return cls._instance
