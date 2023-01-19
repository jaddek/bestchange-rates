from dependency_injector.wiring import Provide
from ..http.safecurrency import Client as SafecurrencyClient, ExchangeRateResponseDTO
from .constants import *
from typing import List

class Fetcher:
    def __init__(self, safecurrency_http_client: SafecurrencyClient = Provide["safecurrency_http_client"]):
        self.__safecurrency_client = safecurrency_http_client

    def fetch(self) -> List[ExchangeRateResponseDTO]:
        result = list()

        self.__fetch_buy_collection(result)
        self.__fetch_sell_collection(result)

        return result

    def __fetch_buy_collection(self, result: list) -> None:
        for fiat, collection in PAIRS_BUY.items():
            for method, crypto in collection.items():
                for coin in crypto:
                    rate = self.__safecurrency_client.get_exchange_rate(
                        from_currency=coin,
                        to_currency=fiat,
                        type=OPERATION_BUY,
                        method=method
                    )

                    result.append(rate)

    def __fetch_sell_collection(self, result: list) -> None:
        for coin, collection in PAIRS_SELL.items():
            for method, fiats in collection.items():
                for fiat in fiats:
                    rate = self.__safecurrency_client.get_exchange_rate(
                        from_currency=coin,
                        to_currency=fiat,
                        type=OPERATION_SELL,
                        method=method
                    )

                    result.append(rate)
