from __future__ import annotations
from typing import Final, List, Literal, Optional, Self, Union
import pandas as pd
from crypto_momentum_portfolios.constants import DATA_FREQUENCY_MAPPER, DATA_PATH
from crypto_momentum_portfolios.indicators import INDICATOR_MAPPING
from crypto_momentum_portfolios.types import (
    CryptoName,
    DataFrequency,
    FieldList,
)


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

    _instance: Optional[Self] = None
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

    def __select_cryptos(
        self,
        crypto_name: Union[Union[CryptoName, Literal["all"]], List[CryptoName]] = "all",
    ) -> pd.DataFrame:
        """Extract the wanted cryptos from the data loader. The method can return a dataframe of multiple crypto series. You can use the `all` keyword to get all the crypto series. To check the crypto available use the `assets` property.

        Args:
        ----
            crypto_name (Union[Union[CryptoName, Literal[&quot;all&quot;]], List[CryptoName]], optional): Whether you want to get a single crypto history, several cryptos or even the whole cryptos of the universe with `all`. Defaults to "all".

        Raises:
        ----
            ValueError: The crypto_name must be a string or a list of strings or even 'all'

        Returns:
        ----
            pd.DataFrame: The dataframe of the wanted cryptos.
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

    def get_crypto(
        self,
        crypto_name: Union[Union[CryptoName, Literal["all"]], List[CryptoName]] = "all",
        data_frequency: DataFrequency = "daily",
        fields: list[FieldList] = ["price"],
        flatten_fields_with_crypto: bool = False,
        **kwargs,
    ) -> pd.DataFrame:
        """Factory method to get crypto data from the data loader. The method can return a single crypto series or a dataframe of multiple crypto series. You can use the `all` keyword to get all the crypto series. To check the crypto available use the `assets` property.

        Args:
        ----
            crypto_name (Union[Union[CryptoName, Literal[&quot;all&quot;]], List[CryptoName]], optional): Whether you want to get a single crypto history, several cryptos or even the whole cryptos of the universe with `all`. Defaults to "all".
            data_frequency (DataFrequency, optional): The wanted frequency for the data. It uses `asfreq` function. Defaults to "daily".
            fields (list[FieldList], optional): The fields to retrieve, the default field that will always be retrvied is price. Defaults to None.
            flatten_fields_with_crypto (bool, optional): Whether to flatten the crypto's names and the fields. If this field is true the result has not a MultiIndex. e.g.: BTC_price, BTC_momentum... Defaults to False.


            **kwargs: The optional arguments to pass to the indicators functions it could be : `momentum_lookback`, `volatility_lookback`

        Returns:
        ----
            pd.DataFrame The crypto dataframe with multiindex columns if `flatten_fields_with_crypto` is False. The first level contains the field (price, returns, ...) and the second the crypto name.
        """
        # Extract the wanted cryptos and resample the data to the wanted frequency
        df = self.__select_cryptos(crypto_name=crypto_name).asfreq(
            DATA_FREQUENCY_MAPPER.get(data_frequency, "1D")
        )

        result = self.___construct_indicators_dataframe(df, fields=fields, **kwargs)
        if flatten_fields_with_crypto:
            result.columns = (
                result.columns.get_level_values(1)
                + "_"
                + result.columns.get_level_values(0)
            )
        return result

    @property
    def assets(self) -> list[str]:
        """Property to get the list of cryptos available in the data loader.

        Returns:
            list[str]: The list of cryptos available in the data loader.
        """
        return self.__assets

    @staticmethod
    def ___construct_indicators_dataframe(
        crypto_dataframe: pd.DataFrame, fields: list[FieldList] = ["price"], **kwargs
    ) -> pd.DataFrame:
        """Handle the indicators to compute on the initial crypto data.

        Args:
        ----
            crypto_dataframe (pd.DataFrame): The crypto data.
            fields (list[FieldList]): The list of indicators to compute.

            **kwargs: The optional arguments to pass to the indicators functions it could be : `momentum_lookback`, `volatility_lookback`

        Returns:
        ----
            pd.DataFrame: The crypto data with the indicators and the multiindex columns.
        """
        # Prepare the final dataframe that has a multiindex columns for each field
        # Make a copy so we are sure not to modify the original dataframe
        df_final = crypto_dataframe.copy()
        # Creating the default price column multiindex
        df_final.columns = pd.MultiIndex.from_product(
            [["price"], crypto_dataframe.columns]
        )

        # Handle the indicators to unique fields
        unique_fields = set(fields)
        # Remove the default field : price
        unique_fields.remove("price")

        assert unique_fields.issubset(
            INDICATOR_MAPPING.keys()
        ), f"Invalid field name, please use one of the following : {','.join(INDICATOR_MAPPING.keys())},"

        for field in unique_fields:
            # Compute the wanted indicator in the mapping dict for the given initial crypto_dataframe (w/o multiindex)
            df_indicator = INDICATOR_MAPPING[field](crypto_dataframe, **kwargs)
            df_indicator.columns = pd.MultiIndex.from_product(
                [[field], crypto_dataframe.columns]
            )  # Create the multiindex columns for this indicator
            # Merge the indicator dataframe with the final dataframe
            df_final = pd.merge(
                df_final,
                df_indicator,
                left_index=True,
                right_index=True,
            )
        return df_final

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
        return raw_dataframe.set_index("date").asfreq("1D")

    def __new__(cls) -> Self:
        """Singleton pattern to get the data loader instance.

        Returns:
        ----
            Self: The only one allowed data loader instance.
        """
        if cls._instance is None:
            cls._instance = super(CryptoDataLoader, cls).__new__(cls)
        return cls._instance
