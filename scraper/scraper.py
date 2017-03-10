import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time
import pickle

def get_player_urls(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    soup = BeautifulSoup(urlopen(url).read(), "lxml")
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
    distance_df['FGA'] = distance_df['FGA'].astype(int) + 1
    distance_df['FG%'] = distance_df['FG%'].astype(float) + 0.001
    soup = BeautifulSoup(html, "lxml")
    name = soup.title.string.replace(' 2016-17 Shooting | Basketball-Reference.com', '')
    return name, distance_df
    
def make_shooting_url(baseurl):
    baseurl = os.path.splitext(baseurl)[0]
    return 'http://www.basketball-reference.com' + baseurl + '/shooting/2017/'
    
def make_league_dicts(year, cache=True):
    urls = get_player_urls(year)
    FGA_dict = {}
    FGpercent_dict = {}
    for url in urls:
        url = make_shooting_url(url)
        attempts = 0
        while attempts < 5:
            try:
                name, df = get_player_stats(url)
                FGA_dict[name] = list(df['FGA'])
                FGpercent_dict[name] = list(df['FG%'])
                break
            except:
                print(url)
                attempts +=1
                time.sleep(10)
    if cache == True:
        pickle.dump(FGA_dict, open("data/FGA.p", "wb"))
        pickle.dump(FGpercent_dict, open("data/FG%.p", "wb"))
    return FGA_dict, FGpercent_dict
    
def append_missing_data(dist_dict, appender):
    for key in dist_dict.keys():
        while len(dist_dict[key]) < 5:
            dist_dict[key].append(appender)
    return dist_dict
            
def make_league_dfs(cache=True):
    FGA = pickle.load(open("data/FGA.p", "rb"))
    FGP = pickle.load(open("data/FG%.p", "rb"))
    FGA = append_missing_data(FGA, 1)
    FGP = append_missing_data(FGP, 0.001)
    FGA = pd.DataFrame.from_dict(FGA).transpose()
    FGP = pd.DataFrame.from_dict(FGP).transpose()
    cols = ['At Rim', '3 to <10 ft', '10 to <16 ft', '16 ft to <3-pt', '3-pt']
    FGA.columns = cols
    FGP.columns = cols
    if cache:
        FGA.to_csv('data/FGA.csv')
        FGP.to_csv('data/FGP.csv')
    return FGA, FGP

if __name__ == '__main__':
    YEAR = 2017
    make_league_dicts(YEAR, cache=True)
    make_league_dfs(cache=True)