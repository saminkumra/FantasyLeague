import numpy as np
import pandas as pd

class Data:
    def __init__(self):
        self.players_data = {}
        self.players_data_column = {}
        self.players_data_attributes = ['id', 'first_name', 'second_name', 'team', 'element_type', 'now_cost',
                                        'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets',
                                        'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
                                        'yellow_cards', 'red_cards', 'saves', 'bonus']
        i = 0
        for column_name in self.players_data_attributes:
            self.players_data_column[column_name] = i
            i += 1

        self.teams_data = {}
        self.prev_teams_data = {}
        self.teams_data_column = {}
        self.teams_data_attributes = ['id', 'name', 'played', 'win', 'draw', 'loss', 'points', 'position',
                                      'strength_attack_away', 'strength_attack_home', 'strength_defence_away',
                                      'strength_defence_home', 'strength_overall_away', 'strength_overall_home']
        i = 0
        for column_name in self.teams_data_attributes:
            self.teams_data_column[column_name] = i
            i += 1

        self.player_gw_data_column = {}
        self.player_gw_data_attributes = ['assists', 'bonus', 'bps', 'clean_sheets', 'goals_conceded', 'goals_scored',
                                          'minutes', 'opponent_team', 'own_goals', 'penalties_missed',
                                          'penalties_saved', 'red_cards', 'saves', 'minutes', 'team_h_score',
                                          'team_a_score', 'total_points', 'value', 'was_home']
        i = 0
        for column_name in self.player_gw_data_attributes:
            self.player_gw_data_column[column_name] = i
            i += 1

    def load_data(self):
        players_path = 'Fantasy-Premier-League/data/2020-21/players_raw.csv'
        players_data = pd.read_csv(players_path)
        players_data = players_data.loc[:, self.players_data_attributes]
        players_data = players_data.to_numpy()

        for row in players_data:
            self.players_data[row[self.players_data_column['id']]] = row

        teams_path = 'Fantasy-Premier-League/data/2020-21/teams.csv'
        teams_data = pd.read_csv(teams_path)
        # Probably want the following data: goals for, goals against, and goal difference
        teams_data = teams_data.loc[:, self.teams_data_attributes]
        teams_data = teams_data.to_numpy()

        for row in teams_data:
            self.teams_data[row[self.teams_data_column['id']]] = row

        prev_teams_path = 'Fantasy-Premier-League/data/2019-20/teams.csv'
        prev_teams_data = pd.read_csv(prev_teams_path)
        prev_teams_data = prev_teams_data.loc[:, self.teams_data_attributes]
        prev_teams_data = prev_teams_data.to_numpy()

        for row in prev_teams_data:
            self.prev_teams_data[row[self.teams_data_column['id']]] = row

    def get_opponent_team_data(self, team_id):
        return self.teams_data[team_id]

    def get_player_gw_data(self, player_id):
        # The following is a test to obtain player gameweek (gw) data for 2019-20 (previous season)
        # TODO: Corroborate this player data with the team the player plays for,
        # which is the 'team' field in players_data
        player_gw_path = get_player_gw_path(self.players_data[player_id][self.players_data_column['first_name']],
                                            self.players_data[player_id][self.players_data_column['second_name']],
                                            self.get_previous_player_id(player_id, '2019-20'))
        player_gw_data = pd.read_csv(player_gw_path)
        player_gw_data = player_gw_data.loc[:, self.player_gw_data_attributes]
        return player_gw_data.to_numpy()

    # A player's ID most likely changes from season to season, so this function returns a player's previous
    # ID from a specified season given his current ID
    def get_previous_player_id(self, current_id, season='2019-20'):
        first_name = self.players_data[current_id][self.players_data_column['first_name']]
        second_name = self.players_data[current_id][self.players_data_column['second_name']]

        # Fetch player ID list from desired season
        id_path = 'Fantasy-Premier-League/data/' + season + '/player_idlist.csv'
        id_data = pd.read_csv(id_path)
        id_data = id_data.to_numpy()

        for row in id_data:
            if first_name == row[0] and second_name == row[1]:
                # If full name matches, return previous player ID
                return row[2]

        # If no match found, return ID number -1
        return -1

    # This function returns the previous season's data for the team ID specified
    def get_previous_team_data(self, current_team_id):
        name = self.teams_data[current_team_id][self.teams_data_column['name']]

        for key in self.prev_teams_data:
            # Search by name is necessary because a team's ID most likely changes from season to season
            if self.prev_teams_data[key][self.teams_data_column['name']] == name:
                return self.prev_teams_data[key]

        return None

    # This function returns a numpy array of a player's opponent difficulties, adjusted for the player's position
    # and whether the player is playing at home or away
    # For example, for a forward at home, the opponent difficulty is a reflection of the opposition's defensive
    # strength when away
    def get_opponent_difficulties(self, player_id):
        player_gw_data = self.get_player_gw_data(player_id)
        opponent_difficulties = np.array([])

        for gw in player_gw_data:
            opponent_team = self.prev_teams_data[gw[self.player_gw_data_column['opponent_team']]]

            # If player is a goalkeeper or defender and playing at home
            if (self.players_data[player_id][self.players_data_column['element_type']] == 1
                or self.players_data[player_id][self.players_data_column['element_type']] == 2)\
                    and gw[self.player_gw_data_column['was_home']]:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[8])

            # If player is a goalkeeper or defender and playing away
            elif (self.players_data[player_id][self.players_data_column['element_type']] == 1
                  or self.players_data[player_id][self.players_data_column['element_type']] == 2)\
                    and not gw[self.player_gw_data_column['was_home']]:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[9])

            # If player is a midfielder or attacker and playing at home
            elif (self.players_data[player_id][self.players_data_column['element_type']] == 3
                  or self.players_data[player_id][self.players_data_column['element_type']] == 4)\
                    and gw[self.player_gw_data_column['was_home']]:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[10])

            # If player is a midfielder or attacker and playing away
            else:
                opponent_difficulties = np.append(opponent_difficulties, opponent_team[11])

        return opponent_difficulties

# Function to generate datapath to gameweek data for the specified player
def get_player_gw_path(first_name, second_name, player_id):
    # Note this is 2019-20 because there is no player data for the new season yet
    return 'Fantasy-Premier-League/data/2019-20/players/' + first_name + '_' + second_name + '_'\
           + str(player_id) + '/gw.csv'
