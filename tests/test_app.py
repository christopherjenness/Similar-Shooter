import pytest
from app import app


@pytest.fixture
def fixed_app():
    ss_app = app
    return ss_app


@pytest.fixture
def test_client(fixed_app):
    return fixed_app.test_client()


def test_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_similar_shooter(test_client):
    response = test_client.post('/result',
                                data={'playername': 'DeAndre Jordan'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Rudy Gobert' in str(response.data)
    assert 'Kyle Korver' not in str(response.data)
