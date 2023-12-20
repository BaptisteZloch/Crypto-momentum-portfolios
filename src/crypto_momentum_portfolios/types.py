from typing import Literal


CryptoName = Literal[
    "date",
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
]

FieldList = Literal[
    "price", "returns", "momentum", "volatility", "instantaneous_volatility"
]

DataFrequency = Literal["daily", "weekly", "monthly"]
