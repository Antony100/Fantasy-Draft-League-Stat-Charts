import json
from unittest import mock

import pytest

import draft

@pytest.fixture
def mock_request(monkeypatch):
    """
    GIVEN a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    class MockResponse(object):
        def __init__(self):
            self.status_code = 200
            self.url = 'http://www.mockleague.com'

        def json(self):
            return {'account': '5678',
                    'url': 'http://www.mockleague.com'}

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(draft.requests, 'get', mock_get)

@pytest.fixture
def mock_league(monkeypatch):
    """
    GIVEN a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    class MockResponse(object):
        def __init__(self):
            self.status_code = 200
            self.url = 'http://www.mockleague.com'

        def json(self):
            with open("/home/tony/projects/dl/sample_league.json", "r") as f:
                data = json.load(f)
            return data

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(draft.requests, 'get', mock_get)

def test_get_player_ids(mock_league):
    d = draft.DraftData(123456)
    assert d.get_player_ids() == {
        'Alan': 11111, 'Bob': 22221, 'Colin': 33331, 'David': 44441,
        'Eric': 55551, 'Frank': 66661, 'Gary': 77771, 'Harry': 88881
    }
    
def test_get_api_data(mock_request):
    d = draft.DraftData(123456)
    assert d.get_api_data() == {'account': '5678',
                    'url': 'http://www.mockleague.com'}