from utils import *
from data_loader import file_ids
import os
import pandas as pd
import gdown


class CloudGaming:
    def __init__(
        self,
        user_id="0116f41a-28b1-4d81-b250-15d7956e2be1",
        time_interval=["2022/07/10" - "2022/08/10"],
    ):
        # TODO: reset the time at the beginning of the program,
        # and update the time every five minutes
        #
        # >>>>>>>>>>>>>>>>>>> UPD. Done <<<<<<<<<<<<<<<<<
        self.user_id = user_id
        self.time_interval = time_interval
        self.initial_system_time = datetime.datetime.now()

        gdown.download(id=file_ids[0], output=f"file_{0}.csv")
        self.current_data = pd.read_csv(f"file_{0}.csv")
        self.current_data["timestamp"] = pd.to_datetime(
            self.current_data["timestamp"]
        )  # convert column to datetime

        self.user_data = self.current_data[
            self.current_data["client_user_id"] == self.user_id
        ]

        self.start_date = self.current_data.iloc[0]["timestamp"]
        self.current_day = 1

        # TODO: 1. Add the data updates every 5 mins
        #       2. Add self.current_data
        # Ultimately, self.interval_data is different from the self.current_data
        # self.interval_data is the data in the given interval, but some of this
        # data might not have fetched yet.
        # Similarly, self.current_data is the data that is currently fetched
        # depending on the time.
        #
        # >>>>>>>>>>>>>>>>>>> UPD. Done <<<<<<<<<<<<<<<<<

    def update_query_data(self, *args):
        """
        Update the query given new data
        """
        self.user_id = args[0]
        self.user_data = self.current_data[
            self.current_data["client_user_id"] == self.user_id
        ]
        if len(args > 1):
            self.time_interval = args[1]

    def load_data(self, range_dates):
        """
        Fetches the data from a give time interval
        """

        for idx in range_dates:
            gdown.download(id=file_ids[idx], output=f"file_{idx}.csv")
            temp_df = pd.read_csv(f"file_{idx}.csv")
            self.current = pd.concat([self.current_data, temp_df], ignore_index=True)

        return self.current_data

    def get_num_sessions(self):
        """
        Gets the number of sessions for a given user
        """
        dfgroup = self.current_data[
            self.interval_data["client_user_id"] == self.user_id
        ].groupby("session_id")
        num_sessions = len(dfgroup)
        return num_sessions

    def get_session(self, session_idx):
        """
        Get the first or the most recent session depending on the given index.
        For example:
                    session_idx = 0, for the first session of a given user
                    session_idx = -1, for the last session of a given user
        """
        datetime_str = self.current_data[
            self.current_data["client_user_id"] == self.user_id
        ].iloc[session_idx]["timestamp"]
        date = datetime.datetime.strptime(datetime_str, f"%Y-%m-%d %H:%M:%S").date()
        return date

    def avg_spent_per_session(self, user_id):
        """
        Get the average time per session in the given df,
        and also returns the sum of all time spent across all sessions
        """
        user_data = self.current_data[self.current_data["client_user_id"] == user_id]
        sessions = user_data["session_id"].unique()

        total = 0
        for session in sessions:
            get_date = lambda datetime_str: datetime.datetime.strptime(
                datetime_str, f"%Y-%m-%d %H:%M:%S"
            )
            session_start = get_date(
                user_data[user_data["session_id"] == session].iloc[0]["timestamp"]
            )
            session_end = get_date(
                user_data[user_data["session_id"] == session].iloc[-1]["timestamp"]
            )
            diff = session_start - session_end
            total += diff.total_seconds()

        avg = avg // len(sessions)
        return avg, total

    def get_most_used_device(self):

        user_df = self.current_data[self.current_data["client_user_id"] == self.user_id]

        devices = dict(user_df["device"].value_counts())
        devices_used = list(devices.keys())
        most_used_device = sorted(devices.items(), key=lambda item: item[1])[-1][0]

        return devices_used, most_used_device

    def is_super_user(self):
        """
        Get the user data for the last 7 days
        """
        user_df = self.current_data[self.current_data["client_user_id"] == self.user_id]
        while current_date <= user_df["timestamp"].iloc[len(user_df) - 1]:
            print(current_date)
            week_data = user_df[
                user_df["timestamp"].between(
                    current_date,
                    current_date + datetime.timedelta(days=7),
                    inclusive=False,
                )
            ]
            time_spent_this_week = self.avg_spent_per_session(week_data)
            current_date = current_date + datetime.timedelta(days=1)
            if time_spent_this_week[1] > 3600:
                return True
        return False

    def get_statistics(self):
        """
        Average of :
                1) Round trip time (RTT)
                2) Frames per Second
                3) Dropped Frames
                4) bitrate
        """
        user_df = self.current_data[self.current_data["client_user_id"] == self.user_id]
        groupby_df = user_df.groupby(["client_user_id"]).mean()
        print("Average Round trip time (RTT) :", float(groupby_df["RTT"]))
        print("Average Frames per Second :", float(groupby_df["FPS"]))
        print("Average Dropped Frames :", float(groupby_df["dropped_frames"]))
        print("Average bitrate:", float(groupby_df["bitrate"]))

    @save_to_file
    def get_status_of_last_week(self, save_to_txt=True):

        # Get the number of sessions
        current_date = self.time_interval.iloc[0]["timestamp"]
        sessions = self.interval_data[
            self.interval_data["timestamp"].between(
                current_date - datetime.timedelta(days=7), current_date, inclusive=False
            )
        ].groupby("session_id")
        num_sessions = len(sessions)
        print(f"The number of sessions is: {num_sessions}")

        session_time_stats = self.avg_spent_per_session(self.interval_data)
        # Get avg time per session
        avg_time_per_session = format_time(session_time_stats[0])
        print(avg_time_per_session)

        # Get sum hours spent by all users
        total_time_spent = format_time(session_time_stats[1])
        print(total_time_spent)

    def fetch_data(self, system_timestep=5):
        # TODO: When the user sends a request to fetch
        # Only fetch upon request, to avoid dealing with bg processes
        num_days_to_fetch = (
            datetime.datetime.now() - self.initial_system_time
        ).total_seconds() // (system_timestep)
        print(
            f"Time elapsed so far: {datetime.datetime.now() - self.initial_system_time}"
        )
        print(f"{num_days_to_fetch} days elapsed since the start of the system")

        self.current_data = self.load_data(
            [
                self.start_date,
                self.start_date + datetime.timedelta(days=num_days_to_fetch),
            ]
        )
        self.user_data = self.current_data[
            self.current_data["client_user_id"] == self.user_id
        ]

    def predict_next_session_time(self):
        return self.avg_spent_per_session(self.user_data)[0]

    @save_to_file
    def print_user_summary(self, save_to_txt=True):
        """
        Prints the user summary, which includes the following:
            * Number of sessions
            * Date of first session
            * Date of most recent session
            * Average time spent per session
            * Most frequently used device
            * Devices used
            * Average of : 1) Round trip time (RTT) 2) Frames per Second 3) Dropped Frames 4) bitrate
            * Total number of bad sessions (predicted using ML model)
            * Estimated next session time
            * Super user or Not (a user who has sessions time more than 60 min in a week)
        """
        if self.user_data.empty:
            print("User not Found try again\n")
        else:
            print("User found!!\n")
            print(f"User with id : {self.user_id}")
            print(f"\tNumber of sessions : {self.get_num_sessions()}")
            print(f"\tDate of first session : {self.get_session(0)}")
            print(
                f"\tAverage time spent per session : {format_time(self.avg_spent_per_session(self.user_data)[0])}"
            )
            print(f"\tDate of most recent session : {self.get_session(-1)}")
            print(f"Most frequently used device : {self.get_most_used_device()[1]}")
            print(f"Devices used : {self.get_most_used_device()[0]}")
            print(
                f"Estimated next session time : {self.avg_spent_per_session(self.user_data)[0]}"
            )
            print(f"Super user : {self.is_super_user()}")
            self.get_statistics()

    def rank_users_by_gaming_time(self):
        get_dict = lambda y: dict((self.avg_spent_per_session(x), len(x)) for x in y)
        times_spent = get_dict(self.current_data["client_user_id"].unique())
        ranked_list = list(
            sorted(times_spent.items(), key=lambda item: item[1], reverse=True)
        )[:5]
        i = 0
        print(f"Rank{' ' * 20}User id{' ' * 18}Time spent gaming")
        for item in ranked_list:
            user_id = item[0]
            time_spent_gaming = item[1]
            print(f"{i}\t{user_id}\t\t{time_spent_gaming}")
            i += 1
