import pytest
from shotchart.shotchart import get_player_urls, get_shot_data, \
    make_shotchart, make_shooting_url


@pytest.fixture
def data():
    top = [0, 1, 2, 3]
    left = [4, 5, 6]
    result = ['Made', 'Missed', 'Missed']
    return (top, left, result)


def test_get_player_urls():
    years = [2015, 2016, 2017]
    for year in years:
        urls = get_player_urls(year)
        assert len(urls) > 300 and len(urls) < 1000
        assert urls['K. Leonard'] == '/players/l/leonaka01.html'


def test_get_shot_data():
    url = 'http://www.basketball-reference.com/players/a/adamsst01/shooting/2017'
    top, left, result = get_shot_data(url)
    assert len(top) == len(left) == len(result)
    assert len(top) > 100


def test_make_shooting_url():
    baseurl = '/players/a/adamsst01'
    target_url = 'http://www.basketball-reference.com/players/a/adamsst01/shooting/2017/'
    test_url = make_shooting_url(baseurl)
    assert target_url == test_url
