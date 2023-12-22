from typing import Literal


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

DataFrequency = Literal["daily", "end_week", "monthly"]

RebalanceFrequency = Literal[
    "daily",
    "weekly",
    "monthly",
    "friday",
    "thursday",
    "wednesday",
    "tuesday",
    "monday",
    "sunday",
    "saturday",
    "month_end",
    "month_start",
    "quarter_end",
    "quarter_start",
    "week_start",
    "week_end",
]
