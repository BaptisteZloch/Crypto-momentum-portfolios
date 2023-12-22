import platform


if platform.system() == "Windows":
    DATA_PATH = "..\\data\\daily_crypto_data.csv"
else:
    DATA_PATH = "../data/daily_crypto_data.csv"


DATA_FREQUENCY_MAPPER = {"daily": "1D", "weekly": "1W", "monthly": "1M"}

REBALANCE_FREQUENCY_MAPPER = {
    "daily": "1D",
    "weekly": "1W",
    "monthly": "1M",
    "friday": "W-FRI",
    "thursday": "W-THU",
    "wednesday": "W-WED",
    "tuesday": "W-TUE",
    "monday": "W-MON",
    "sunday": "W-SUN",
    "saturday": "W-SAT",
    "month_end": "1M",
    "month_start": "MS",
    "quarter_end": "Q",
    "quarter_start": "QS",
    "week_start": "1W",
    "week_end": "W-FRI",
}
