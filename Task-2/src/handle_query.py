# Assuming that we have all the data now and the user is querying
# At the last day.
from utils import *

import os
import pandas as pd


def load_data(time_interval):
    # TODO: Load the data that is relavant to the current interval
    def get_date_from_filename(filename):
        date_splitted = "_".join(filename.split('.')[0].split('_')[1:])
        parsed_date = parse_date(date_splitted, '_')
        return parsed_date


    df_in_interval = pd.DataFrame()
    dir = "/Users/husseinyounes/University/Python/SDP-Assignment-2/Task-2/data/SSD2022AS2"
    for filename in sorted(os.listdir(dir)):
        date = get_date_from_filename(filename)
        if time_interval[0] <= date <= time_interval[1]:
            print(f'{date} in interval')
            current_df = pd.read_csv(os.path.join(dir, filename))
            print(current_df.shape)
            df_in_interval = pd.concat([df_in_interval, current_df])
            print(df_in_interval.shape)
            
    return df_in_interval


def get_sessions(user_id, time_interval):
    pass


def get_status_of_last_week():
    pass


def print_summary(user_id, time_interval, save_txt=True):
    pass


def predict_next_session(user_id):
    pass
