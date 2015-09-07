import pytest
from etherpadlite.client import EtherpadClient

@pytest.fixture(scope='module')
def client():
    return EtherpadClient(base_url='http://localhost:9001/api/1.2.12', api_key='8e2d3a1030753d0e481f179fc450b126a30dff14e18794331cd238d32d921056')