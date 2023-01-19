import click
from flask.cli import with_appcontext
from dependency_injector.wiring import Provide, inject
from package.rate.fetcher import Fetcher


@click.command(name='fetch')
@with_appcontext
@inject
def create_user(fetcher: Fetcher = Provide['fetcher']):
    result = fetcher.fetch()

    print(result)