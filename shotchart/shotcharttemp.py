from urllib.request import urlopen
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import seaborn.apionly as sns
import os
import time
import sys
import re

def get_player_urls(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    soup = BeautifulSoup(urlopen(url).read(), "lxml")
    urls = {}
    for anchor in soup.findAll('a', href=True):
        if anchor['href'].startswith('/players/') and len(anchor['href']) > 10:
            urls[anchor.text] = anchor['href']
    return urls


def get_shot_data(url):
    html = str(urlopen(url).read())
    top = re.findall ( 'top:(.*?)px;', html, re.DOTALL)
    left = re.findall ( 'left:(.*?)px;', html, re.DOTALL)
    result = re.findall ( 'remaining<br>(.*?) ', html, re.DOTALL)
    return top, left, result
    
def make_shotchart(top, left, result, player_name, cache=True):
    plt.figure()
    df = pd.DataFrame({'top': top[1:], 'left': left, 'result': result})
    made = df[df.result=='Made']
    missed = df[df.result=='Missed']

    im = plt.imread('court.png')
    implot = plt.imshow(im)
    
    plt.scatter(list(missed.left), list(missed.top), c=sns.color_palette()[2], alpha=0.7, linewidths=0)
    plt.scatter(list(made.left), list(made.top), c=sns.color_palette()[1], alpha=0.7, linewidths=0)
    plt.axis('off')
    if cache==True:
        plt.savefig('images/' + player_name)
    else:
        plt.show()
    plt.close()

def make_shooting_url(baseurl):
    baseurl = os.path.splitext(baseurl)[0]
    return 'http://www.basketball-reference.com' + baseurl + '/shooting/2017/'

def save_shot_charts(year):
    url_dict = get_player_urls(year)
    for player, url in url_dict.items():
        url = make_shooting_url(url)
        attempts = 0
        while attempts < 5:
            try:
                top, left, result = get_shot_data(url)
                make_shotchart(top, left, result, player, cache=True)
                break
            except:
                print(url)
                print("Unexpected error:", sys.exc_info()[0])
                attempts += 1
                time.sleep(10)



YEAR = 2017

"""
url = 'http://www.basketball-reference.com/players/h/hardeja01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'James Harden')

YEAR = 2017
url = 'http://www.basketball-reference.com/players/d/duranke01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'Kevin Durant')

url = 'http://www.basketball-reference.com/players/c/curryst01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'Stephen Curry')

url = 'http://www.basketball-reference.com/players/w/wadedw01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'Dwyane Wade')

url = 'http://www.basketball-reference.com/players/j/jamesle01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'LeBron James')

url = 'http://www.basketball-reference.com/players/n/nowitdi01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'Dirk Nowitzki')
"""

url = 'http://www.basketball-reference.com/players/h/howardw01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'Dwight Howard')

"""
url = 'http://www.basketball-reference.com/players/h/hardeja01/shooting/2017/'
top, left, results = get_shot_data(url)
make_shotchart(top, left, results, 'James Harden')
"""

