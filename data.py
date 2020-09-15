import numpy as np
import csv
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class Data:
    def __init__(self):
        self.players_data = {}
        self.players_data_attributes = ['id', 'first_name', 'second_name', 'team', 'element_type', 'now_cost',
                                        'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets',
                                        'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
                                        'yellow_cards', 'red_cards', 'saves', 'bonus']
        self.teams_data = {}
        self.teams_data_attributes = ['id', 'name', 'played', 'win', 'draw', 'loss', 'points', 'position',
                                      'strength_attack_away', 'strength_attack_home', 'strength_defence_away',
                                      'strength_defence_home', 'strength_overall_away', 'strength_overall_home']
        self.player_gw_data_attributes = ['assists', 'bonus', 'bps', 'clean_sheets', 'goals_conceded', 'goals_scored',
                                          'minutes', 'opponent_team', 'own_goals', 'penalties_missed',
                                          'penalties_saved', 'red_cards', 'saves', 'minutes', 'team_h_score',
                                          'team_a_score', 'total_points', 'value', 'was_home']
        self.prev_teams_data = {}

    def load_data(self):
        players_path = 'Fantasy-Premier-League/data/2020-21/players_raw.csv'
        players_data = pd.read_csv(players_path)
        players_data = players_data.loc[:, self.players_data_attributes]
        players_data = players_data.to_numpy()

        for row in players_data:
            self.players_data[row[0]] = row

        teams_path = 'Fantasy-Premier-League/data/2020-21/teams.csv'
        teams_data = pd.read_csv(teams_path)
        # Probably want the following data: goals for, goals against, and goal difference
        teams_data = teams_data.loc[:, self.teams_data_attributes]
        teams_data = teams_data.to_numpy()

        for row in teams_data:
            self.teams_data[row[0]] = row

        prev_teams_path = 'Fantasy-Premier-League/data/2019-20/teams.csv'
        prev_teams_data = pd.read_csv(prev_teams_path)
        prev_teams_data = prev_teams_data.loc[:, self.teams_data_attributes]
        prev_teams_data = prev_teams_data.to_numpy()

        for row in prev_teams_data:
            self.prev_teams_data[row[0]] = row

    def get_opponent_team_data(self, team_id):
        return self.teams_data[team_id]

    def get_player_gw_data(self, player_id):
        # The following is a test to obtain player gameweek (gw) data for 2019-20 (previous season)
        # TODO: Corroborate this player data with the team the player plays for,
        # which is the 'team' field in players_data
        player_gw_path = get_player_gw_path(self.players_data[player_id][1], self.players_data[player_id][2],
                                            self.get_previous_player_id(player_id, '2019-20'))
        player_gw_data = pd.read_csv(player_gw_path)
        player_gw_data = player_gw_data.loc[:, self.player_gw_data_attributes]
        return player_gw_data.to_numpy()

    def get_previous_player_id(self, current_id, season):
        first_name = self.players_data[current_id][1]
        second_name = self.players_data[current_id][2]
        id_path = 'Fantasy-Premier-League/data/' + season + '/player_idlist.csv'
        id_data = pd.read_csv(id_path)
        id_data = id_data.to_numpy()
        for row in id_data:
            if first_name == row[0] and second_name == row[1]:
                return row[2]
        return -1

    def get_previous_team_data(self, current_team_id):
        name = self.teams_data[current_team_id][1]
        for key in self.prev_teams_data:
            if self.prev_teams_data[key][1] == name:
                return self.prev_teams_data[key]
        return None

    def get_opponent_difficulties(self, player_id):
        player_gw_data = self.get_player_gw_data(player_id)
        opponent_difficulties = np.array([])
        for gw in player_gw_data:
            opponent_team = self.prev_teams_data[gw[7]]
            if (self.players_data[player_id][4] == 1 or self.players_data[player_id][4] == 2) and gw[-1]:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[8])
            elif (self.players_data[player_id][4] == 1 or self.players_data[player_id][4] == 2) and not gw[-1]:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[9])
            elif (self.players_data[player_id][4] == 3 or self.players_data[player_id][4] == 4) and gw[-1]:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[10])
            else:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[11])
        return opponent_difficulties

def get_player_gw_path(first_name, second_name, player_id):
    # Note this is 2019-20 because there is no player data for the new season yet
    return 'Fantasy-Premier-League/data/2019-20/players/' + first_name + '_' + second_name + '_'\
           + str(player_id) + '/gw.csv'
tester = Data()
tester.load_data()
print(tester.get_player_gw_data(4))
print(tester.get_previous_team_data(13))
print(tester.get_opponent_difficulties(4))

opponent_difficulties = tester.get_opponent_difficulties(24).reshape(-1, 1)
player_points = tester.get_player_gw_data(24)[:, -3].reshape(-1, 1)
print(player_points)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(opponent_difficulties, player_points)
Y_pred = linear_regressor.predict(opponent_difficulties)
plt.scatter(opponent_difficulties, player_points)
plt.plot(opponent_difficulties, Y_pred, color='red')
plt.show()

# TODO: Some things to think about here
# Maybe for each metric (goals, assists, bonus; total), we can plot the data points on the y axis against strength on
# the x. For defenders, the x axis would be opponent attacking strength. For attackers, the x axis would be opponent
# defending strength. Find some way to incorporate home/away. Maybe use the difference between the strengths of the 2
# sides in a match?
# Then maybe the model would be best served as a linear regression model