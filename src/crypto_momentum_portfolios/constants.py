import platform


if platform.system() == "Windows":
    DATA_PATH = "..\\data\\daily_crypto_data.csv"
else:
    DATA_PATH = "../data/daily_crypto_data.csv"


DATA_FREQUENCY_MAPPER = {"daily": "1D", "weekly": "1W", "monthly": "1M"}


