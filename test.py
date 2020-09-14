import requests
import pandas as pd
import numpy as np

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json_obj = r.json()

elements_df = pd.DataFrame(json_obj['elements'])
elements_types_df = pd.DataFrame(json_obj['element_types'])
teams_df = pd.DataFrame(json_obj['teams'])

slim_elements_df = elements_df[['second_name','team','element_type','selected_by_percent','now_cost','minutes',
                                'transfers_in','value_season','total_points']]
print(slim_elements_df)