import json
from pathlib import Path
from urllib.parse import urlparse

import pytest
import requests
from pact import Pact
from pact import Verifier

CONSUMER = "user-consumer"
PROVIDER = "user-provider"
SERVICE = "https://fakeapi.in"
BROKER = "http://localhost:9292"
PACT_DIR = Path(__file__).parent / "pacts"



@pytest.fixture
def pact():
    pact = Pact(CONSUMER, PROVIDER).with_specification("V4")
    yield pact
    pact.write_file(PACT_DIR)


def test_pact(pact: Pact):

    response = _generate_pact_from_service(pact, method="GET", path="/api/users/1")
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == 1
    assert body["name"] == "Jonathan Considine"

    response = _publish_pact_to_broker()
    assert response.status_code in (200, 201)

    _verify_pact_against_service()

    response = _test_with_pact_server(pact, method="GET", path="/api/users/1")
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == 1
    assert body["name"] == "Jonathan Considine"

def _generate_pact_from_service(pact:Pact, method:str, path:str):

    response = requests.request(method, SERVICE + path)

    (pact.upon_receiving(f"A '{method}' request for path '{path}'")
    .with_request(
        method=method,
        path=path,
    ).will_respond_with(response.status_code)
    #.with_headers(dict(response.headers))  # changing time in headers can cause validation to fail
    .with_body(
        response.content.decode()
    ))

    return response

def _publish_pact_to_broker():

    with open(PACT_DIR / f"{CONSUMER}-{PROVIDER}.json") as f:
        pact = json.load(f)

    url = f"{BROKER}/pacts/provider/{PROVIDER}/consumer/{CONSUMER}/version/1.0.0"

    response = requests.put(url, json=pact)

    return response

def _verify_pact_against_service():

    verifier = (
        Verifier(PROVIDER, host=urlparse(SERVICE).hostname)  # default host is localhost
        .add_transport(url=SERVICE)
        .broker_source(BROKER)
    )

    verifier.verify()


def _test_with_pact_server(pact: Pact, method:str, path:str):

    with pact.serve() as srv:
        return requests.request(method, str(srv.url) + path)