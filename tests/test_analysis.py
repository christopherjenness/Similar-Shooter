from analysis.analysis import load_data, get_similar_shooters


def test_get_similar_shooters():
    FGA, FGP = load_data()
    similar_shooters = get_similar_shooters('DeAndre Jordan', FGA, FGP)
    top_similar = list(similar_shooters.sort_values('KL-divergence').head()['player'])
    assert 'Rudy Gobert' in top_similar
    assert 'Kyle Korver' not in top_similar


def test_load_data():
    FGA, FGP = load_data()
    assert list(FGA.loc['Aaron Gordon']) == [188, 61, 60, 90, 199]
