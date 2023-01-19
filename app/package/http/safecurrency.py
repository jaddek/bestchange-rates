import http.client as http_client
import json


class ValidationErrorsDTO:
    """Validation error response scheme"""

    def __init__(self, errors: dict):
        self.errors = errors


class ExchangeRateResponseDTO:
    """Rate response scheme"""

    __map = {
        'from': 'from_currency',
        'to': 'to_currency',
        'in': 'in_amount'
    }

    def __init__(self, body: dict):
        self.amount = body.get('amount')
        self.type = body.get('type')
        self.from_currency = body.get('fromCurrency')
        self.to_currency = body.get('toCurrency')
        self.rate = body.get('rate')
        self.method = body.get('method')
        self.total_amount = body.get('totalAmount')
        self.in_amount: str = '1'

    def __getattr__(self, item) -> str:
        if self.__map.get(item):
            return getattr(self, self.__map.get(item))
        elif hasattr(self, item):
            return getattr(self, item)
        else:
            return 'None'


class HttpResponseException(Exception):
    """Common response scheme"""

    def __init__(self, http_status, body):
        self.http_status = http_status
        self.body = body

    def get_response_body(self) -> dict:
        return self.body


class HttpValidationException(HttpResponseException):
    """Validation exception"""

    def get_response_body(self) -> dict:
        return json.loads(self.body.decode())['errors']


class Client:
    """HTTP client for transmitting rate data from safecurrency API"""
    DEFAULT_HEADERS = {
        "Content-Type": "application/json"
    }

    def __init__(self, host: str, secure: bool = True):
        self.host = host
        self._init_request(host, secure)

    def _init_request(self, host: str, secure: bool):
        if secure:
            self.http_client = http_client.HTTPSConnection(host)
        else:
            self.http_client = http_client.HTTPConnection(host)

    def get_exchange_rate(self, from_currency: str, to_currency: str, type: str, method: str):
        body = json.dumps({
            'type': type,
            'from': from_currency,
            'to': to_currency,
            'amount': '1',
            'method': method,
        })

        self.http_client.request(
            method="POST",
            url="/api/v1/exchange/rates/export",
            headers=self.DEFAULT_HEADERS,
            body=body
        )

        response = self.http_client.getresponse()

        '''if response is json:'''
        body = json.loads(response.read().decode())
        http_status_code = response.getcode()

        if http_status_code == 200:
            return ExchangeRateResponseDTO(body)
        elif http_status_code == 422:
            raise HttpValidationException(http_status_code, body)
        else:
            raise HttpResponseException(http_status_code, body)
