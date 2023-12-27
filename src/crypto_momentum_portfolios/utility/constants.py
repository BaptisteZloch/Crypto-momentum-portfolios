import platform

CRYPTOS = {
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
    "ATOM-USDT",
    "KDA-USDT",
    "VET-USDT",
    "EOS-USDT",
}


if platform.system() == "Windows":
    DATA_PATH = "..\\data_from_TOBAM\\daily_crypto_data.csv"
else:
    DATA_PATH = "../data_from_TOBAM/daily_crypto_data.csv"


TRANSACTION_COST = 0.001  # Binance taker spot fees
SLIPPAGE_EFFECT = 0.0005  # 0.05% slippage effect


PERCENT_METRICS = [
    "Expected return",
    "CAGR",
    "Expected volatility",
    "VaR",
    "CVaR",
    "Max drawdown",
    "Kelly criterion",
    "Expectancy",
    "Specific risk",
    "Systematic risk",
    "Tracking error",
]
