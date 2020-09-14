import numpy as np
import csv
import os
import pandas as pd

#def load_data(data_path):
path = 'Fantasy-Premier-League/data/2020-21/cleaned_players.csv'

position_data = pd.read_csv(path)
position_data = position_data.loc[:, 'element_type']
position_data =  position_data.to_numpy()

path2 = 'Fantasy-Premier-League/data/2020-21/players_raw.csv'
raw_data = pd.read_csv(path2)
raw_data = raw_data.loc[:, ['first_name', 'second_name', 'team', 'now_cost', 'total_points', 'minutes',
                 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved',
                'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus']]
raw_data = raw_data.to_numpy()

players_data = np.concatenate((raw_data, np.reshape(position_data, (-1, 1))), axis=1)
print(players_data)
