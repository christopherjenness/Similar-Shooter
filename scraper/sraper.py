import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_player_urls(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    soup = BeautifulSoup(urlopen(url).read())
    urls = []
    for anchor in soup.findAll('a', href=True):
        if anchor['href'].startswith('/players/') and len(anchor['href']) > 10:
            urls.append(anchor['href'])
    return list(set(urls))
    
def get_player_stats(url):
    html = str(urlopen(url).read())
    df = pd.read_html(html)[0]
    distance_df = df[df[1].isin(['At Rim', '3 to <10 ft', '10 to <16 ft', '16 ft to <3-pt', '3-pt'])]
    distance_df = distance_df[[1, 3, 4]]
    distance_df.columns = ['Distance', 'FGA', 'FG%']
    return distance_df
    


b = get_player_stats('http://www.basketball-reference.com/players/a/adamsst01.html')


url = 'http://www.basketball-reference.com/players/a/adamsst01/shooting/2017/'
b = get_player_stats(url)

a = pd.read_html(html)
b = a[0]
b.head(100)
b.to_csv('test.csv')
b[b[1].isin(['At Rim', '3 to <10 ft', '10 to <16 ft', '16 ft to <3-pt', '3-pt'])]
