from dependency_injector.wiring import Provide, inject
from flask import Response
from package.xml import build_rate_xml
from package.rate.fetcher import Fetcher
from package.rate.transformer import transform_collection


@inject
def index(fetcher: Fetcher = Provide["fetcher"]):
    result = fetcher.fetch()
    xml = build_rate_xml(transform_collection(result))
    return Response(xml, mimetype='text/xml')
