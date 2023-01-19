from ..http.safecurrency import ExchangeRateResponseDTO as SafecurrencyRateDTO
from .constants import *
from .remains import Remains
from typing import TypeVar, List


class BestChangeDTO:
    def __init__(
            self,
            _to: str,
            _from: str,
            _in: str,
            out: str,
            minamount: str,
            maxamount: str,
            amount: str
    ):
        self.__to = _to
        self.__from = _from
        self.__in = _in
        self.__out = out
        self.__minamount = minamount
        self.__maxamount = maxamount
        self.__amount = amount

    def get_to(self):
        return self.__to.__str__()

    def get_from(self):
        return self.__from.__str__()

    def get_in(self):
        return self.__in.__str__()

    @property
    def out(self):
        return self.__out.__str__()

    @property
    def minamount(self):
        return self.__minamount.__str__()

    @property
    def maxamount(self):
        return self.__maxamount.__str__()

    @property
    def amount(self):
        return self.__amount.__str__()

    def get_dict(self) -> dict:
        return {
            'from': self.get_from(),
            'to': self.get_to(),
            'in': self.get_in(),
            'out': self.out,
            'minamount': self.minamount,
            'maxamount': self.maxamount,
            'amount': self.amount
        }


T = TypeVar('T', bound=SafecurrencyRateDTO)
TBC = TypeVar('TBC', bound=BestChangeDTO)

def transform_collection(rates: List[T]) -> List[TBC]:
    transformer = BestChangeTransformer()

    for i in range(len(rates)):
        rates[i] = transformer(rates[i])

    return rates

class BestChangeTransformer:
    def __call__(self, *args, **kwargs):
        return self.__transform(*args)

    def __transform(self, dto: SafecurrencyRateDTO) -> object:
        if dto.type == OPERATION_SELL:
            dto = BestChangeDTO(
                _to=self.__transform_currency(dto.to_currency, dto.method),
                _from=self.__transform_currency(dto.from_currency, dto.method),
                _in=dto.in_amount,
                out=dto.total_amount,
                minamount=Remains.get_min_amount(dto.from_currency),
                maxamount=Remains.get_max_amount(dto.from_currency),
                amount=Remains.get_amount(dto.to_currency)
            )
        else:
            dto = BestChangeDTO(
                _to=self.__transform_currency(dto.from_currency, dto.method),
                _from=self.__transform_currency(dto.to_currency, dto.method),
                _in=dto.in_amount,
                out=dto.total_amount,
                minamount=Remains.get_min_amount(dto.to_currency),
                maxamount=Remains.get_max_amount(dto.to_currency),
                amount=Remains.get_amount(dto.from_currency)
            )

        return dto

    @staticmethod
    def __transform_currency(currency: str, method: str) -> str:
        is_prefix_required: bool = currency in FIAT

        if is_prefix_required and method.lower() == METHOD_SEPA.lower():
            return SEPAEUR

        if is_prefix_required:
            return FIAT_PREFIX + currency

        return currency
