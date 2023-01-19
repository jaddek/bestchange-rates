import os
from dependency_injector import containers, providers
from package.http.safecurrency import Client as SafecurrencyClient
from package.rate.fetcher import Fetcher

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "views", "package.rate.fetcher", "commands"
    ])

    safecurrency_http_client = providers.Singleton(
        SafecurrencyClient,
        host=os.getenv('SAFECURRENCY_HOST'),
        secure=True
    )

    fetcher = providers.Singleton(
        Fetcher,
        safecurrency_http_client=safecurrency_http_client
    )
