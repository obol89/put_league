import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_post_valid_teams(client):
    teams = [f"Team {chr(65 + i)}" for i in range(16)]
    response = client.post('/', data={'teams': json.dumps(teams), 'group_count': '4'})
    assert response.status_code == 200


def test_post_no_teams(client):
    response = client.post('/')
    assert response.status_code == 400


def test_post_invalid_json(client):
    response = client.post('/', data={'teams': 'not valid json'})
    assert response.status_code == 400


def test_post_empty_team_name(client):
    teams = ["Valid Name", "   "]
    response = client.post('/', data={'teams': json.dumps(teams)})
    assert response.status_code == 400


def test_post_too_long_team_name(client):
    teams = ["Valid", "A" * 33]
    response = client.post('/', data={'teams': json.dumps(teams)})
    assert response.status_code == 400


def test_post_special_chars_allowed(client):
    teams = ["FC Barca #1", "Team @Home"]
    response = client.post('/', data={'teams': json.dumps(teams)})
    assert response.status_code == 200


def test_post_too_few_teams(client):
    teams = ["Only One"]
    response = client.post('/', data={'teams': json.dumps(teams)})
    assert response.status_code == 400


def test_post_invalid_group_count(client):
    teams = [f"Team {chr(65 + i)}" for i in range(16)]
    # 5 doesn't evenly divide 16
    response = client.post('/', data={'teams': json.dumps(teams), 'group_count': '5'})
    assert response.status_code == 400


def test_post_group_size_too_small(client):
    teams = [f"Team {chr(65 + i)}" for i in range(4)]
    # 4 groups of 1 team each — too small
    response = client.post('/', data={'teams': json.dumps(teams), 'group_count': '4'})
    assert response.status_code == 400


def test_teams_without_session(client):
    response = client.get('/teams')
    assert response.status_code == 302


def test_summary_without_session(client):
    response = client.get('/summary')
    assert response.status_code == 302


def test_full_flow_16_teams(client):
    teams = [f"Team {chr(65 + i)}" for i in range(16)]
    response = client.post('/', data={'teams': json.dumps(teams), 'group_count': '4'})
    assert response.status_code == 200

    response = client.get('/teams')
    assert response.status_code == 200
    assert b'Group A' in response.data

    response = client.get('/summary')
    assert response.status_code == 200
    assert 'text/csv' in response.content_type
    assert b'Group stage' in response.data


def test_full_flow_8_teams_2_groups(client):
    teams = [f"Team {chr(65 + i)}" for i in range(8)]
    response = client.post('/', data={'teams': json.dumps(teams), 'group_count': '2'})
    assert response.status_code == 200

    response = client.get('/teams')
    assert response.status_code == 200
    assert b'Group A' in response.data
    assert b'Group B' in response.data

    response = client.get('/summary')
    assert response.status_code == 200
    assert 'text/csv' in response.content_type


def test_full_flow_default_group_size(client):
    """When no group_count is provided, default to groups of 4."""
    teams = [f"Team {chr(65 + i)}" for i in range(16)]
    response = client.post('/', data={'teams': json.dumps(teams)})
    assert response.status_code == 200

    response = client.get('/teams')
    assert response.status_code == 200
    assert b'Group A' in response.data


def test_404_page(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
