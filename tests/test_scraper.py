import mock
from scraper.scraper import get_player_urls, get_player_stats, \
    make_shooting_url, make_league_dicts, append_missing_data, \
    make_league_dfs


def test_get_player_urls():
    years = [2015, 2016, 2017]
    for year in years:
        urls = get_player_urls(year)
        assert len(urls) > 300 and len(urls) < 1000
        assert isinstance(urls[0], str)


def test_get_player_stats():
    url = 'http://www.basketball-reference.com/players/a/adamsst01/shooting/2017'
    name, distance_df = get_player_stats(url)
    assert name == 'Steven Adams'
    assert distance_df.shape == (5, 3)

    
def test_make_shooting_url():
    baseurl = '/players/a/adamsst01'
    shooting_url = make_shooting_url(baseurl)
    assert shooting_url == 'http://www.basketball-reference.com/players/a/adamsst01/shooting/2017/'


def mock_league_urls(*args):
    mock_urls = ['/players/a/adamsst01', '/players/g/greendr01']
    return mock_urls


@mock.patch('scraper.scraper.get_player_urls', new=mock_league_urls)
def test_make_league_dicts():
    FGA_dict, FGpercent_dict = make_league_dicts(2017, cache=False)
    assert 'Steven Adams' in FGA_dict.keys()
    assert FGA_dict['Steven Adams'] == [379, 267, 34, 4, 3]


def test_append_missing_data():
    dist_dict = {10: []}
    new_dict = append_missing_data(dist_dict, 10)
    assert new_dict == {10: [10, 10, 10, 10, 10]}


def test_make_league_dfs():
    FGA, FGP = make_league_dfs(cache=False)
    assert list(FGA.loc['Zaza Pachulia']) == [145, 33, 15, 21, 1]
