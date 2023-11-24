from __future__ import annotations
from typing import Final, List, Literal, Optional, Self, Union
import pandas as pd
from crypto_momentum_portfolios.constants import DATA_PATH
from crypto_momentum_portfolios.types import CryptoName


class CryptoDataLoader:
    """
    CryptoDataLoader is a singleton class for loading and managing crypto data.

    Protected Attributes:
    ----
        _instance (Optional[CryptoDataLoader]): The singleton instance of CryptoDataLoader.


    Private Attributes:
    ----
        __PATH (Final): The path to the crypto data CSV file.
        __data (pd.DataFrame): The wrangled crypto data.
        __assets (List[str]): The list of crypto assets.

    Methods:
    ----
        __init__(): Initialize the CryptoDataLoader instance.
        __load_data() -> pd.DataFrame: Load and wrangle crypto data from the CSV file.
        get_crypto(crypto_name: Union[Union[CryptoName, Literal["all"]], List[CryptoName]]) -> Union[pd.Series, pd.DataFrame]:
            Factory method to get crypto data from the data loader.
        assets() -> List[str]: Get the list of available crypto assets.
        __wrangle_data(raw_dataframe: pd.DataFrame) -> pd.DataFrame: Perform data wrangling on raw dataframe.
        __new__() -> Self: Singleton pattern to get the data loader instance.
    """

    _instance: Optional[CryptoDataLoader] = None
    __PATH: Final = DATA_PATH

    def __init__(self):
        self.__data = self.__load_data()
        self.__assets = self.__data.columns.to_list()

    def __load_data(self) -> pd.DataFrame:
        """Get the crypto data from the csv file and wrangle it.

        Returns:
            pd.DataFrame: The wrangled crypto data.
        """
        return self.__wrangle_data(pd.read_csv(self.__PATH))

    def get_crypto(
        self,
        crypto_name: Union[Union[CryptoName, Literal["all"]], List[CryptoName]] = "all",
    ) -> Union[pd.Series, pd.DataFrame]:
        """Factory method to get crypto data from the data loader. The method can return a single crypto series or a dataframe of multiple crypto series. You can use the `all` keyword to get all the crypto series. To check the crypto available use the `assets` property.

        Args:
        ----
            crypto_name (Union[Union[CryptoName, Literal[&quot;all&quot;]], List[CryptoName]], optional): Whether you want to get a single crypto history, several cryptos or even the whole cryptos of the universe with `all`. Defaults to "all".

        Raises:
        ----
            ValueError: The crypto_name must be a string or a list of strings or even 'all'

        Returns:
        ----
            Union[pd.Series, pd.DataFrame]: The crypto series or dataframe of crypto series.
        """
        if crypto_name == "all":
            return self.__data
        elif isinstance(crypto_name, list):
            return self.__data[crypto_name]
        elif isinstance(crypto_name, str):
            return self.__data[[crypto_name]]
        else:
            raise ValueError(
                f"Invalid crypto_name: {crypto_name} must be a string or a list of strings or even 'all'"
            )

    @property
    def assets(self) -> list[str]:
        """Property to get the list of cryptos available in the data loader.

        Returns:
            list[str]: The list of cryptos available in the data loader.
        """
        return self.__assets

    @staticmethod
    def __wrangle_data(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
        """Perform data wrangling on raw dataframe the steps are :
        - Convert date column to datetime
        - Set date column as index

        Args:
        ----
            raw_dataframe (pd.DataFrame): The raw dataframe from a csv file.

        Returns:
        ----
            pd.DataFrame: The wrangled dataframe.
        """
        raw_dataframe["date"] = pd.to_datetime(
            raw_dataframe["date"], infer_datetime_format=True
        )
        raw_dataframe = raw_dataframe.set_index("date")
        return raw_dataframe.asfreq("1D")

    def __new__(cls) -> Self:
        """Singleton pattern to get the data loader instance.

        Returns:
        ----
            Self: The only one allowed data loader instance.
        """
        if cls._instance is None:
            cls._instance = super(CryptoDataLoader, cls).__new__(cls)
        return cls._instance
