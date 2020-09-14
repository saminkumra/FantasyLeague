import numpy as np
import csv
import os
import pandas as pd

# def load_data(data_path):
# Column 'element_type' from players_raw.csv is actually the position, just as numeric code rather than a String

players_path = 'Fantasy-Premier-League/data/2020-21/players_raw.csv'
players_data = pd.read_csv(players_path)
players_data = players_data.loc[:, ['id', 'first_name', 'second_name', 'team', 'element_type', 'now_cost',
                                    'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets',
                                    'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
                                    'yellow_cards', 'red_cards', 'saves', 'bonus']]
players_data = players_data.to_numpy()

print(players_data)

teams_path = 'Fantasy-Premier-League/data/2020-21/teams.csv'
team_data = pd.read_csv(teams_path)
# Probably want goals for, goals against, and goal difference
team_data = team_data.loc[:, ['id', 'name', 'played', 'win', 'draw', 'loss', 'points', 'position',
                              'strength_attack_away', 'strength_attack_home', 'strength_defence_away',
                              'strength_defence_home', 'strength_overall_away', 'strength_overall_home']]
print(team_data)