"""
Scripts for determining players with similar shot charts.
Workhorse of analysis is Kullback-Leibler divergence for comparin distributions
https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence
"""

import pandas as pd
from scipy.stats import entropy


def load_data(min_shots=250):
    """
    Loads shot data from csv

    Args:
        min_shots (Int): Minimum number of shots required to
            retain player in data

    Returns: (df.DataFrame, df.DataFrame)
        tuple of pd.DataFrames of FGA and FG% for various court
            locations for each player
    """
    FGA = (pd.read_csv('data/FGA.csv')
           .set_index('Unnamed: 0'))
    FGP = (pd.read_csv('data/FGP.csv')
           .set_index('Unnamed: 0'))
    players = FGA[FGA.sum(axis=1) > min_shots].index.values
    FGA = FGA[FGA.index.isin(players)]
    FGP = FGP[FGP.index.isin(players)]
    return FGA, FGP


def get_similar_shooters(target_player, FGA_df, FGP_df):
    """
    Finds similar shot chart for target_player via KL-divergence
    of FGA distributions

    Args:
        target_player (str): Player to find similar shot charts for
        FGA_df (pd.DataFrame): DataFrame of FGA distributions by
            court location for each player
        FGP_df (pd.DataFrame): DataFrame of FG% distributions by
             court location for each player

    Returns: pd.DataFrame
        DataFrame with cols [player (str), KL-divergence (float)]
        Each row is how similar each player is to the target player
        Smaller KL-divergence indicates a closer match in shot chart
    """
    players = FGA_df.index.values
    target_FGA = list(FGA_df[FGA_df.index.values == target_player].values[0])
    data = []
    for player in players:
        if player != target_player:
            test_FGA = list(FGA_df[FGA_df.index.values == player].values[0])
            KL = entropy(target_FGA, test_FGA)
            data.append([player, KL])
    FGA_comparisons = pd.DataFrame(data, columns=["player", "KL-divergence"])
    return FGA_comparisons
