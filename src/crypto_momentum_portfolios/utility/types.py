from typing import Literal
from enum import IntEnum, StrEnum

CryptoName = Literal[
    "bitcoin",
    "ethereum",
    "bitcoin_cash",
    "ripple",
    "litecoin",
    "tron",
    "ethereum_classic",
    "chainlink",
    "stellar",
    "cardano",
    "dash",
    "tezos",
    "binancecoin",
    "solana",
    "matic_network",
    "dogecoin",
    "avalanche_2",
    "BTC-USDT",
    "ETH-USDT",
    "BCH-USDT",
    "XRP-USDT",
    "LTC-USDT",
    "ETC-USDT",
    "TRX-USDT",
    "ADA-USDT",
    "BNB-USDT",
    "SOL-USDT",
    "DASH-USDT",
    "XTZ-USDT",
    "LINK-USDT",
    "XLM-USDT",
    "MATIC-USDT",
    "DOGE-USDT",
    "AVAX-USDT",
]

FieldList = Literal[
    "price",
    "volumne",
    "amount",
    "market_cap",
    "returns",
    "momentum",
    "volatility",
    "instantaneous_volatility",
    "long_ma",
    "short_ma",
    "long_ema",
    "short_ema",
]


class Fields(StrEnum):
    PRICE = "price"
    VOLUME = "volume"
    AMOUNT = "amount"
    MARKET_CAP = "market_cap"
    RETURNS = "returns"
    MOMENTUM = "momentum"
    VOLATILITY = "volatility"
    INSTANTANEOUS_VOLATILITYV = "instantaneous_volatility"
    LONG_MA = "long_ma"
    SHORT_MA = "short_ma"
    LONG_EMA = "long_ema"
    SHORT_EMA = "short_ema"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))


class DataFrequency(StrEnum):
    DAILY = "1D"
    WEEKLY = "1W"
    MONTHLY = "1M"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))


class Side(IntEnum):
    LONG = 1
    SHORT = -1

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))


class RebalanceFrequency(StrEnum):
    DAILY = "1D"
    WEEKLY = "1W"
    MONTHLY = "1M"
    FRIDAY = "W-FRI"
    THURSDAY = "W-THU"
    WEDNESDAY = "W-WED"
    TUESDAY = "W-TUE"
    MONDAY = "W-MON"
    SUNDAY = "W-SUN"
    SATURDAY = "W-SAT"
    MONTH_END = "1M"
    MONTH_START = "MS"
    QUARTER_END = "Q"
    QUARTER_START = "QS"
    WEEK_START = "1W"
    WEEK_END = "W-FRI"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))


class Benchmark(StrEnum):
    EQUAL_WEIGHTED = "equal_weighted_benchmark"
    CAPITALIZATION_WEIGHTED = "capi_weighted_benchmark"
    BITCOIN = "bitcoin_benchmark"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))


class AllocationMethod(StrEnum):
    CAPITALIZATION_WEIGHTED = "capitalization_weighted"
    VOLUME_WEIGHTED = "volume_weighted"
    EQUAL_WEIGHTED = "equal_weighted"
    MOMENTUM_WEIGHTED = "momentum_weighted"
    RISK_PARITY = "risk_parity"
    MEAN_VARIANCE = "mean_variance"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))


class Metrics(StrEnum):
    EXPECTED_RETURN = "Expected return"
    CAGR = "CAGR"
    EXPECTED_VOLATILITY = "Expected volatility"
    SKEWNESS = "Skewness"
    KURTOSIS = "Kurtosis"
    VAR = "VaR"
    CVAR = "CVaR"
    MAX_DRAWDOWN = "Max drawdown"
    KELLY_CRITERION = "Kelly criterion"
    PROFIT_FACTOR = "Profit factor"
    PAYOFF_RATIO = "Payoff ratio"
    EXPECTANCY = "Expectancy"
    SHARPE_RATIO = "Sharpe ratio"
    SORTINO_RATIO = "Sortino ratio"
    BURKE_RATIO = "Burke ratio"
    CALMAR_RATIO = "Calmar ratio"
    TAIL_RATIO = "Tail ratio"
    SPECIFIC_RISK = "Specific risk"
    SYSTEMATIC_RISK = "Systematic risk"
    PORTFOLIO_BETA = "Portfolio beta"
    PORTFOLIO_ALPHA = "Portfolio alpha"
    JENSEN_ALPHA = "Jensen alpha"
    R2 = "R2"
    TRACKING_ERROR = "Tracking error"
    TREYNOR_RATIO = ("Treynor ratio",)
    INFORMATION_RATIO = "Information ratio"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))
