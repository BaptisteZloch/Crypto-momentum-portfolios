import platform


if platform.system() == "Windows":
    DATA_PATH = "..\\data\\daily_crypto_data.csv"
else:
    DATA_PATH = "../data/daily_crypto_data.csv"
