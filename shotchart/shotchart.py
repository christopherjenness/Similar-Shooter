"""
Script to generate shot charts for NBA players
"""

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
    """
    Get BR URLs for all players in a given year

    Args:
        year (int): year to get active players

    Returns: list
        list of BR URLs
    """
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    soup = BeautifulSoup(urlopen(url).read(), "lxml")
    urls = {}
    for anchor in soup.findAll('a', href=True):
        if anchor['href'].startswith('/players/') and len(anchor['href']) > 10:
            urls[anchor.text] = anchor['href']
    return urls

def get_shot_data(url):
    """
    Gets locations and results of all shots for a given URL
    Args:
        url (str): BR URL for a given player's shots
            Example: 'http://www.basketball-reference.com/players/a/adamsst01/shooting/2017/'

    Returns: list, list, list
        3 lists of:
            top (y location)
            left (x location)
            result (string in ['Made', 'Missed'])
    """
    html = str(urlopen(url).read())
    top = re.findall ( 'top:(.*?)px;', html, re.DOTALL)
    left = re.findall ( 'left:(.*?)px;', html, re.DOTALL)
    result = re.findall ( 'remaining<br>(.*?) ', html, re.DOTALL)
    return top, left, result
    
def make_shotchart(top, left, result, player_name, cache=True):
    """
    Makes shotchart of a given player

    Args:
        top (list): list of y coordinates (int) of all shots
        left (list): list of x coordinates (int) of all shots
        result (list): list of results (str in ['Made', 'Missed'] of all shots
        player_name (str): player name
        cache (bool): if True, save plot

    Returns: None
    """
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
    """
    Helper function to turn base url into full shooting URL for a player
    """
    baseurl = os.path.splitext(baseurl)[0]
    return 'http://www.basketball-reference.com' + baseurl + '/shooting/2017/'

def save_shot_charts(year):
    """
    Makes and saves shot charts for all active NBA players in a year

    Args:
        year (int): Year of interest

    Returns: None
    """
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

if __name__ == '__main__':
    YEAR = 2017
    save_shot_charts(YEAR)