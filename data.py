import numpy as np
import csv
import os
import pandas as pd

# test
# def load_data(data_path):

# Column 'element_type' from players_raw.csv is actually the position, just as numeric code rather than a String
# 1 = GK, 2 = DEF, 3 = MID, 4 = FWD

players_path = 'Fantasy-Premier-League/data/2020-21/players_raw.csv'
players_data = pd.read_csv(players_path)
players_data = players_data.loc[:, ['id', 'first_name', 'second_name', 'team', 'element_type', 'now_cost',
                                    'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets',
                                    'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
                                    'yellow_cards', 'red_cards', 'saves', 'bonus']]
players_data = players_data.to_numpy()
print(players_data)

teams_path = 'Fantasy-Premier-League/data/2020-21/teams.csv'
teams_data = pd.read_csv(teams_path)
# Probably want the following data: goals for, goals against, and goal difference
teams_data = teams_data.loc[:, ['id', 'name', 'played', 'win', 'draw', 'loss', 'points', 'position',
                              'strength_attack_away', 'strength_attack_home', 'strength_defence_away',
                              'strength_defence_home', 'strength_overall_away', 'strength_overall_home']]
teams_data = teams_data.to_numpy()
print(teams_data)

# The following is a test to obtain player gameweek (gw) data for 2019-20 (previous season) Aaron Cresswell
# TODO: Corroborate this player data with the team the player plays for, which is the 'team' field in players_data
player_gw_path = 'Fantasy-Premier-League/data/2019-20/players/Aaron_Cresswell_376/gw.csv'
player_gw_data = pd.read_csv(player_gw_path)
player_gw_data = player_gw_data.loc[:, ['assists', 'bonus', 'bps', 'clean_sheets', 'goals_conceded', 'goals_scored',
                                        'minutes', 'opponent_team', 'own_goals', 'penalties_missed', 'penalties_saved',
                                        'red_cards', 'saves', 'minutes', 'team_h_score', 'team_a_score',
                                        'total_points', 'value']]
player_gw_data = player_gw_data.to_numpy()
print(player_gw_data)


def get_player_gw_path(first_name, second_name, id):
    # Note this is 2019-20 because there is no player data for the new season yet
    return 'Fantasy-Premier-League/data/2019-20/players/' + first_name + '_' + second_name + '_' + id + '/gw.csv'

# TODO: Some things to think about here
# Maybe for each metric (goals, assists, bonus; total), we can plot the data points on the y axis against strength on
# the x. For defenders, the x axis would be opponent attacking strength. For attackers, the x axis would be opponent
# defending strength. Find some way to incorporate home/away. Maybe use the difference between the strengths of the 2
# sides in a match?
# Then maybe the model would be best served as a linear regression model