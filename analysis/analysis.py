import pandas as pd
from scipy.stats import entropy



def get_similar_shooters(player_name, FGA_df, FGP_df):
    return




FGA = pd.read_csv('data/FGA.csv')
FGA.columns.values[0] = 'Name'
FGP = pd.read_csv('data/FGP.csv')
FGP.columns.values[0] = 'Name'



print(FGA.head())