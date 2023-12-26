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


class DataFrequency(StrEnum):
    DAILY = "1D"
    WEEKLY = "1W"
    MONTHLY = "1M"


class Side(IntEnum):
    LONG = 1
    SHORT = -1


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


class Benchmark(StrEnum):
    EQUAL_WEIGHTED = "equal_weighted_benchmark"
    CAPITALIZATION_WEIGHTED = "capi_weighted_benchmark"
    BITCOIN = "bitcoin_benchmark"


class AllocationMethod(StrEnum):
    CAPITALIZATION_WEIGHTED = "capitalization_weighted"
    VOLUME_WEIGHTED = "volume_weighted"
    EQUAL_WEIGHTED = "equal_weighted"
    MOMENTUM_WEIGHTED = "momentum_weighted"
    RISK_PARITY = "risk_parity"
    MEAN_VARIANCE = "mean_variance"
