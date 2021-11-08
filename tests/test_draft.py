import pytest
import requests_mock
from requests.exceptions import HTTPError
from unittest.mock import patch

from draft import DraftData, HeadToHead, LeagueStats, BASE_URL


@pytest.fixture
def test_draft():
    return DraftData(123)


@pytest.fixture
def mock_draft_details():
    return {
        # Trimmed data
        "league": {
            "admin_entry": 314726,
        },
        "league_entries": [
            {
                "entry_id": 11111,
                "entry_name": "Team1",
                "id": 11112,
                "joined_time": "2020-08-18T17:39:19.131650Z",
                "player_first_name": "Alan",
                "player_last_name": "Alpha",
                "short_name": "AA",
                "waiver_pick": 8
            },
            {
                "entry_id": 22221,
                "entry_name": "Team2",
                "id": 22222,
                "joined_time": "2020-08-18T18:01:21.685642Z",
                "player_first_name": "Bob",
                "player_last_name": "Bravo",
                "short_name": "BB",
                "waiver_pick": 3
            },
            {
                "entry_id": 33331,
                "entry_name": "Team3",
                "id": 33332,
                "joined_time": "2020-08-19T15:29:54.028633Z",
                "player_first_name": "Colin",
                "player_last_name": "Charlie",
                "short_name": "CC",
                "waiver_pick": 7
            }
        ]
    }


@pytest.fixture
def mock_player_history():
    return {
        'history':
            [
                {
                    'id': 132209,
                    'points': 58,
                    'total_points': 58,
                    'rank': None,
                    'rank_sort': None,
                    'event_transfers': 0,
                    'points_on_bench': 0,
                    'entry': 219110,
                    'event': 1
                },
                {
                    'id': 525419,
                    'points': 61,
                    'total_points': 119,
                    'rank': None,
                    'rank_sort': None,
                    'event_transfers': 0,
                    'points_on_bench': 0,
                    'entry': 219110,
                    'event': 2
                },
                {
                    'id': 984164,
                    'points': 46,
                    'total_points': 165,
                    'rank': None,
                    'rank_sort': None,
                    'event_transfers': 0,
                    'points_on_bench': 0,
                    'entry': 219110,
                    'event': 3
                }
            ]
        }


@pytest.fixture
def mock_player_ids():

    with patch('draft.DraftData.get_player_ids') as m:
        m.return_value = {'Alan': 11111, 'Bob': 22221, 'Colin': 33331}
        yield m


@pytest.fixture
def mock_get_history(mock_player_history):
    with patch('draft.DraftData.get_player_history') as m:
        m.return_value = mock_player_history
        yield m


@pytest.fixture
def mock_get_players_points():
    with patch('draft.DraftData.get_players_points') as m:
        m.return_value = {'Alan': {1: 22}, 'Bob': {1: 33}}
        yield m


@pytest.fixture
def mock_get_players_points_list():
    with patch('draft.DraftData.get_players_points') as m:
        m.return_value = {'Alan': [22, 12, 51], 'Bob': [33, 58, 11]}
        yield m


def test_init_DraftData():
    draft = DraftData(123)

    assert draft.league_id == 123


def test_api_data_defaults(test_draft):
    test_data = {'foo': 'bar'}

    with requests_mock.Mocker() as m:
        m.get(BASE_URL, json=test_data)
        result = test_draft.get_api_data()

    assert m.call_count == 1
    assert m.request_history[0].url == BASE_URL
    assert m.request_history[0].method == 'GET'
    assert result == test_data


def test_api_data_bad_status_code(test_draft):

    with requests_mock.Mocker() as m:
        m.get(BASE_URL, status_code=500)
        with pytest.raises(HTTPError) as error:
            test_draft.get_api_data()

    assert error.value.args[0] == (
        '500 Server Error: None for url: https://draft.premierleague.com/api/'
    )
    assert m.call_count == 1
    assert m.request_history[0].url == BASE_URL
    assert m.request_history[0].method == 'GET'


def test_get_player_ids(test_draft, mock_draft_details):
    url = f'{BASE_URL}league/123/details'

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_draft_details)
        result = test_draft.get_player_ids()

    assert result == {
        'Alan': 11111,
        'Bob': 22221,
        'Colin': 33331,
    }


def test_get_player_history(
    test_draft, mock_player_history, mock_player_ids
):
    url = f'{BASE_URL}entry/11111/history'

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_player_history)
        result = test_draft.get_player_history('Alan')

    assert m.call_count == 1
    assert m.request_history[0].url == url
    assert m.request_history[0].method == 'GET'
    assert result == mock_player_history


def test_get_points_per_gameweek(test_draft, mock_player_history):

    assert test_draft.get_points_per_gameweek(
        mock_player_history) == [58, 61, 46]


def test_get_players_points(test_draft, mock_get_history):

    assert test_draft.get_players_points('alan') == {
        'alan': {1: 58, 2: 61, 3: 46}
        }
    assert test_draft.get_players_points('alan', format_type='list') == {
        'alan': [58, 61, 46]
        }


# HeadToHead Class
def test_HeadToHead_init(mock_get_players_points):

    h2h = HeadToHead(12345, "Alan", "Bob")

    assert h2h.league_id == 12345
    assert h2h.player1 == "Alan"
    assert h2h.player2 == "Bob"
    assert h2h.players_scores == {'Alan': {1: 22}, 'Bob': {1: 33}}


def test_headtohead_score(mock_get_players_points):
    h2h = HeadToHead(12345, "Alan", "Bob")

    assert h2h.headtohead_score() == {'Alan': 0, 'Bob': 1, 'draw': 0}


# LeagueStats Class


def test_LeagueStats_init(mock_player_ids, mock_get_players_points_list):

    ls = LeagueStats(12345)

    assert ls.league_id == 12345
    assert ls.all_player_scores == {'Alan': [22, 12, 51], 'Bob': [33, 58, 11]}


@pytest.mark.parametrize(
    "test_input, expected", [
        ([1, 2, 3, 4], 2), ([0], 0), ([52, 34, 88, 72, 1, 29], 46)
    ]
    )
def test_calc_average(
    test_input, expected, mock_player_ids, mock_get_players_points_list
):
    ls = LeagueStats(12345)
    assert ls.calc_average(test_input) == expected


def test_get_gameweek_statistic(
    mock_player_ids, mock_get_players_points_list
):
    ls = LeagueStats(12345)
    assert ls.get_gameweek_statistic(min) == {'Alan': 12, 'Bob': 11}
    assert ls.get_gameweek_statistic(max) == {'Alan': 51, 'Bob': 58}
    assert ls.get_gameweek_statistic(ls.calc_average) == {
        'Alan': 28, 'Bob': 34
    }
