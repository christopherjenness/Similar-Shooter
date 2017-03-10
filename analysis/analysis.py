import pandas as pd
from scipy.stats import entropy

def load_data(min_shots=250):
    FGA = pd.read_csv('data/FGA.csv')
    FGP = pd.read_csv('data/FGP.csv')
    FGA = FGA.set_index('Unnamed: 0')
    FGP = FGP.set_index('Unnamed: 0')
    players = FGA[FGA.sum(axis=1) > min_shots].index.values
    FGA = FGA[FGA.index.isin(players)]
    FGP = FGP[FGP.index.isin(players)]
    return FGA, FGP

def get_similar_shooters(target_player, FGA_df, FGP_df):
    players = FGA_df.index.values
    target_FGA = list(FGA_df[FGA_df.index.values==target_player].values[0])
    data = []
    for player in players:
        if player != target_player:
            test_FGA = list(FGA_df[FGA_df.index.values==player].values[0])
            KL = entropy(target_FGA, test_FGA)
            data.append([player, KL])
    FGA_comparisons = pd.DataFrame(data, columns=["player", "KL-divergence"])
    return FGA_comparisons



if __name__ == '__main__':
    FGA, FGP = load_data(min_shots=250)
    
    player_name = 'LaMarcus Aldridge'
    a = get_similar_shooters(player_name, FGA, FGP)
    a.sort('KL-divergence', ascending=True).head()





