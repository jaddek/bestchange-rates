from .constants import *
from random import randrange
from typing import Optional


class Remains:
    """
    Remains for limits and amounts
    """
    @staticmethod
    def __get_remains() -> dict:
        return {
            BTC: randrange(50, 70),
            ETH: randrange(10000, 20000),
            XRP: randrange(300000, 350000),
            EUR: randrange(135000, 600000),
            USD: randrange(160000, 290000),
            GBP: randrange(160000, 290000),
        }

    @staticmethod
    def __get_limits():
        return {
            BTC: {
                'min': '0.003 BTC',
                'max': '99999 BTC'
            },
            ETH: {
                'min': '1000 ETH',
                'max': '4300 ETH'
            },
            XRP: {
                'min': '100 XRP',
                'max': '3000 XRP'
            },
            EUR: {
                'min': '25 EUR',
                'max': '250000 EUR'
            },
            USD: {
                'min': '25 USD',
                'max': '250000 USD'
            },
            GBP: {
                'min': '25 GBP',
                'max': '25000 GBP'
            }
        }

    @staticmethod
    def get_min_amount(currency: str) -> str:
        """
        To currency
        :param currency:
        :return:
        """
        return Remains.__get_limits().get(currency, {}).get('min', None)

    @staticmethod
    def get_max_amount(currency: str) -> str:
        """
        To currency
        :param currency:
        :return:
        """
        return Remains.__get_limits().get(currency, {}).get('max', None)

    @staticmethod
    def get_amount(currency: str) -> Optional[str]:
        """
        From currency
        :param currency: 
        :return: 
        """
        return Remains.__get_remains().get(currency, None)
