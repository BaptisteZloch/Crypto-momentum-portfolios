import pandas as pd
import numpy as np
from scipy import stats
from quant_invest_lab.portfolio import construct_report_dataframe

from crypto_momentum_portfolios.utility.constants import PERCENT_METRICS


def print_performance_statistics(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
    perform_t_stats: bool = True,
    n_samples: int = 1000,
    sample_size: int = 200,
    alpha_risk: float = 0.05,
) -> pd.DataFrame:
    assert (
        strategy_returns.shape[0] == benchmark_returns.shape[0]
    ), "Error: different length"
    assert strategy_returns.shape[0] > sample_size, "Error: sample size too large"

    df = pd.concat([strategy_returns, benchmark_returns], axis=1)
    df.columns = ["strategy", "benchmark"]
    # print(df)
    final_stats = construct_report_dataframe(
        df["strategy"], df["benchmark"], timeframe="1day"
    )
    if perform_t_stats:
        bootstrap_strat_returns_stats = pd.DataFrame(
            map(
                lambda sample_index: construct_report_dataframe(
                    portfolio_returns=pd.Series(
                        df.loc[sample_index]["strategy"].to_numpy(),
                        index=benchmark_returns.index[:sample_size],
                    ),
                    # benchmark_returns=pd.Series(
                    #     df.loc[sample_index]["benchmark"].to_numpy(),
                    #     index=benchmark_returns.index[:sample_size],
                    # ),
                    timeframe="1day",
                )["Portfolio"],
                np.random.choice(
                    df.index.to_numpy(), size=(n_samples, sample_size), replace=True
                ),
            )
        )
    for metric in final_stats.index:
        if perform_t_stats is True:
            if metric in bootstrap_strat_returns_stats.columns:
                # if metric in bootstrap_strat_returns_stats.columns:
                t_stat, p_value = stats.ttest_1samp(
                    bootstrap_strat_returns_stats[metric].to_numpy(),
                    popmean=final_stats["Benchmark"][metric],
                )
                print(f"\n{metric:-^50}")
                if metric in PERCENT_METRICS:
                    print(
                        f"Benchmark: {100*final_stats['Benchmark'][metric]:.2f}% vs Strategy: {100*final_stats['Portfolio'][metric]:.2f}%"
                    )
                else:
                    print(
                        f"Benchmark: {final_stats['Benchmark'][metric]:.2f} vs Strategy: {final_stats['Portfolio'][metric]:.2f}"
                    )
                print(f"\nt-stat: {t_stat:.2f}, p-value: {p_value:.2f}")
                print(
                    f"{'Statistically different from the bench' if p_value < alpha_risk else 'Not statistically different from the bench'}"
                )
            else:
                print(f"\n{metric:-^50}")
                if metric in PERCENT_METRICS:
                    print(
                        f"Benchmark: N/A vs Strategy: {100*final_stats['Portfolio'][metric]:.2f}%"
                    )
                else:
                    print(
                        f"Benchmark: N/A vs Strategy: {final_stats['Portfolio'][metric]:.2f}"
                    )
        else:
            print(f"\n{metric:-^50}")
            if metric in PERCENT_METRICS:
                print(
                    f"Benchmark: {100*final_stats['Benchmark'][metric]:.2f}% vs Strategy: {100*final_stats['Portfolio'][metric]:.2f}%"
                )
            else:
                print(
                    f"Benchmark: {final_stats['Benchmark'][metric]:.2f} vs Strategy: {final_stats['Portfolio'][metric]:.2f}"
                )

    return final_stats
