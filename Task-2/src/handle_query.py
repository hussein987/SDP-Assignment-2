from utils import *

import os
import pandas as pd


class CloudGaming:

    def __init__(self, user_id, time_interval):
        # TODO: reset the time at the beginning of the program,
        # and update the time every five minutes
        self.user_id = user_id
        self.time_interval = time_interval
        self.initial_time = datetime.datetime.now()

        self.load_data()





    def load_data(self, time_interval):
        """
        Fetches the data from a give time interval
        """
        # TODO: Load the data that is relavant to the current interval
        def get_date_from_filename(filename):
            date_splitted = "_".join(filename.split(".")[0].split("_")[1:])
            parsed_date = parse_date(date_splitted, "_")
            return parsed_date

        df_in_interval = pd.DataFrame()
        dir = (
            "/Users/husseinyounes/University/Python/SDP-Assignment-2/Task-2/data/SSD2022AS2"
        )
        for filename in sorted(os.listdir(dir)):
            date = get_date_from_filename(filename)
            if time_interval[0] <= date <= time_interval[1]:
                current_df = pd.read_csv(os.path.join(dir, filename))
                df_in_interval = pd.concat([df_in_interval, current_df])

        return df_in_interval


    def get_num_sessions(user_id, time_interval):
        """
        Gets the number of sessions for a given user
        """
        interval_data = load_data(
            [parse_date(time_interval[0], "/"), parse_date(time_interval[1], "/")]
        )
        dfgroup = interval_data[interval_data["client_user_id"] == user_id].groupby(
            "session_id"
        )
        num_sessions = len(dfgroup)
        return num_sessions


    def get_session(user_id, time_interval, session_idx):
        """
        Get the first or the most recent session depending on the given index.
        For example:
                    session_idx = 0, for the first session of a given user
                    session_idx = -1, for the last session of a given user
        """
        interval_data = load_data(
            [parse_date(time_interval[0], "/"), parse_date(time_interval[1], "/")]
        )
        datetime_str = interval_data[interval_data["client_user_id"] == user_id].iloc[
            session_idx
        ]["timestamp"]
        date = datetime.datetime.strptime(datetime_str, f"%Y-%m-%d %H:%M:%S").date()
        return date


    def avg_spent_per_session(user_id, time_interval):
        fetched_data = load_data(
            [parse_date(time_interval[0], "/"), parse_date(time_interval[1], "/")]
        )

        user_df = fetched_data[fetched_data["client_user_id"] == user_id]
        sessions = user_df["session_id"].unique()

        avg = 0
        for session in sessions:
            get_date = lambda datetime_str: datetime.datetime.strptime(
                datetime_str, f"%Y-%m-%d %H:%M:%S"
            )
            first_session = get_date(
                user_df[user_df["session_id"] == session].iloc[0]["timestamp"]
            )
            last_session = get_date(
                user_df[user_df["session_id"] == session].iloc[-1]["timestamp"]
            )
            diff = last_session - first_session
            avg += diff.seconds
        
        avg = avg // len(sessions)
        print(avg)

    def get_most_used_device(user_id, time_interval):
        fetched_data = load_data(
            [parse_date(time_interval[0], "/"), parse_date(time_interval[1], "/")]
        )

        user_df = fetched_data[fetched_data["client_user_id"] == user_id]

        devices = dict(user_df["device"].value_counts())
        devices_used = list(devices.keys())
        most_used_device = sorted(devices.items(), key=lambda item: item[1])[-1][0]

        return devices_used, most_used_device


    def is_super_user(user_id):
        time

    def get_status_of_last_week():
        pass


    def print_summary(user_id, time_interval, save_txt=True):
        pass


    def predict_next_session(user_id):
        pass


    def fetch_data():
        pass
