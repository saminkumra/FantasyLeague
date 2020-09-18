from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import data

tester = data.Data()
tester.load_data()
#print(tester.get_player_gw_data(4))
#print(tester.get_previous_team_data(13))
#print(tester.get_opponent_difficulties(4))

opponent_difficulties = tester.get_opponent_difficulties(254).reshape(-1, 1)
player_points = tester.get_player_gw_data(254)[:, -3].reshape(-1, 1)
#print(player_points)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(opponent_difficulties, player_points)
Y_pred = linear_regressor.predict(opponent_difficulties)
plt.scatter(opponent_difficulties, player_points)
plt.plot(opponent_difficulties, Y_pred, color='red')
plt.show()

# TODO: Some things to think about here
# Maybe for each metric (goals, assists, bonus; total), we can plot the data points on the y axis against strength on
# the x.