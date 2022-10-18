from tkinter import E
from utils import *
from data_loader import file_ids
import pandas as pd
import gdown


class CloudGaming:
    def __init__(
        self,
        user_id="0116f41a-28b1-4d81-b250-15d7956e2be1",
        time_interval=["2022/07/10", "2022/08/10"],
    ):
        # TODO: reset the time at the beginning of the program,
        # and update the time every five minutes
        #
        # >>>>>>>>>>>>>>>>>>> UPD. Done <<<<<<<<<<<<<<<<<
        self.user_id = user_id
        self.time_interval = time_interval
        self.initial_system_time = datetime.datetime.now()

        clear_data()
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
        if len(args) > 1:
            self.time_interval = args[1]

    def load_data(self, range_dates):
        """
        Fetches the data from a give time interval
        """

        for idx in range(range_dates[0], range_dates[1]):
            if idx >= len(file_ids):
                print("No more data available to fetch")
                break
            gdown.download(id=file_ids[idx], output=f"file_{idx}.csv")
            temp_df = pd.read_csv(f"file_{idx}.csv")
            temp_df["timestamp"] = pd.to_datetime(
                temp_df["timestamp"]
            )  # convert column to datetime
            self.current_data = pd.concat([self.current_data, temp_df], ignore_index=True)

        return self.current_data

    def get_num_sessions(self):
        """
        Gets the number of sessions for a given user
        """
        dfgroup = self.user_data[
            self.user_data["timestamp"].between(
                self.time_interval[0], self.time_interval[1], inclusive=False
            )
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
        interval_data = self.user_data[
            self.user_data["timestamp"].between(
                self.time_interval[0], self.time_interval[1], inclusive=False
            )
        ]
        if not interval_data.empty:
            date = interval_data.iloc[session_idx]["timestamp"]
        else:
            return "There are not sessions in the given interval"
        return date

    def avg_spent_per_session(self, user_id=None, df=None, check_interval=False):
        """
        Get the average time per session in the given df,
        and also returns the sum of all time spent across all sessions
        """
        if df is None:
            user_df = self.current_data[self.current_data["client_user_id"] == user_id]
            if check_interval:
                df = user_df[
                    user_df["timestamp"].between(
                        self.time_interval[0], self.time_interval[1], inclusive=False
                    )
                ]
            else:
                df = user_df
            if df.empty:
                    return "There are no relevant data in the given interval"
            sessions = df["session_id"].unique()
        else:
            sessions = df["session_id"].unique()

        total = 0
        for session in sessions:
            session_start = df[df["session_id"] == session].iloc[0]["timestamp"]
            session_end = df[df["session_id"] == session].iloc[-1]["timestamp"]
            diff = session_end - session_start
            total += diff.total_seconds()

        avg = total // len(sessions)
        return avg, total

    def get_most_used_device(self):

        user_df = self.current_data[self.current_data["client_user_id"] == self.user_id]

        devices = dict(user_df["device"].value_counts())
        devices_used = list(devices.keys())
        most_used_device = sorted(devices.items(), key=lambda item: item[1])[-1][0]

        return devices_used, most_used_device

    def is_super_user(self):
        """
        Find out whether the given user is a super user.
        Note:
            A super user is a user who has sessions time more than 60 min in a week.
        """
        user_df = self.current_data[self.current_data["client_user_id"] == self.user_id]
        current_date = user_df.iloc[0]['timestamp']
        while current_date <= user_df["timestamp"].iloc[-1]:
            week_data = user_df[
                user_df["timestamp"].between(
                    current_date,
                    current_date + datetime.timedelta(days=7),
                    inclusive=False,
                )
            ]
            time_spent_this_week = self.avg_spent_per_session(df=week_data)
            current_date = current_date + datetime.timedelta(days=7)
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
        groupby_df = self.user_data[self.user_data['timestamp'].between(
                self.time_interval[0], self.time_interval[1], inclusive=False
            )].groupby(["client_user_id"]).mean()
        if not groupby_df.empty:
            print("\tAverage Round trip time (RTT) :", float(groupby_df["RTT"]))
            print("\tAverage Frames per Second :", float(groupby_df["FPS"]))
            print("\tAverage Dropped Frames :", float(groupby_df["dropped_frames"]))
            print("\tAverage bitrate:", float(groupby_df["bitrate"]))

    @save_to_file
    def get_status_of_last_week(self, save_txt=True):

        # Get the number of sessions from week back till now
        current_date = self.current_data.iloc[-1]["timestamp"]
        interval_data = self.current_data[
            self.current_data["timestamp"].between(
                current_date - datetime.timedelta(days=6),
                current_date + datetime.timedelta(days=1),
                inclusive=False,
            )
        ]
        sessions = interval_data.groupby("session_id")

        # Get num sessions
        num_sessions = len(sessions)
        print(f"Total sessions : {num_sessions}")

        # Get avg time spent per session
        session_time_stats = self.avg_spent_per_session(df=interval_data)
        avg_time_per_session = format_time(session_time_stats[0])
        print(f"Average time spent per session : {avg_time_per_session}")

        # Get sum hours spent by all users
        total_time_spent = format_time(session_time_stats[1])
        print(f"Sum of hours spent by all users : {total_time_spent}\n")

    def fetch_data(self, system_timestep=5):
        # TODO: When the user sends a request to fetch
        # Only fetch upon request, to avoid dealing with bg processes.
        #
        # >>>>>>>>>>>>>>>>>>> UPD. Done <<<<<<<<<<<<<<<<<
        num_days_to_fetch = int((
            datetime.datetime.now() - self.initial_system_time
        ).total_seconds() // (system_timestep)) - self.current_day
        print(
            f"\nTime elapsed so far: {datetime.datetime.now() - self.initial_system_time}"
        )
        print(f"{num_days_to_fetch} days elapsed since the last update\n")

        self.current_data = self.load_data(
            [self.current_day, self.current_day + num_days_to_fetch]
        )
        self.user_data = self.current_data[
            self.current_data["client_user_id"] == self.user_id
        ]
        self.current_day += num_days_to_fetch

    def predict_next_session_time(self):
        if self.user_data.empty:
            return "There's no dat found for the given user id"
        return self.avg_spent_per_session(df=self.user_data)[0]

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
            print("\nUser found!!")
            print(f"User with id : {self.user_id}")
            print(f"\tNumber of sessions : {self.get_num_sessions()}")
            print(f"\tDate of first session : {self.get_session(0)}")
            user_session_stats = self.avg_spent_per_session(user_id=self.user_id, check_interval=True)
            if not type(user_session_stats) == str:
                print(
                    f"\tAverage time spent per session : {format_time(self.avg_spent_per_session(user_id=self.user_id, check_interval=True)[0])}"
                )
            print(f"\tDate of most recent session : {self.get_session(-1)}")
            print(f"\tMost frequently used device : {self.get_most_used_device()[1]}")
            print(f"\tDevices used : {self.get_most_used_device()[0]}")
            if not type(user_session_stats) == str:
                print(
                    f"\tEstimated next session time : {format_time(self.avg_spent_per_session(user_id=self.user_id, check_interval=True)[0])}"
                )
            if type(user_session_stats) == str:
                print("\tSuper user : This user has no sessions in the given time interval")
            else:
                print(f"\tSuper user : {self.is_super_user()}")
            self.get_statistics()

    def rank_users_by_gaming_time(self):
        get_dict = lambda y: dict((x, self.avg_spent_per_session(user_id=x)[1]) for x in y)
        times_spent = get_dict(self.current_data["client_user_id"].unique())
        ranked_list = list(
            sorted(times_spent.items(), key=lambda item: item[1], reverse=True)
        )[:5]
        i = 0
        print(f"Rank{' ' * 20}User id{' ' * 18}Time spent gaming")
        for item in ranked_list:
            user_id = item[0]
            time_spent_gaming = item[1]
            print(f"{i}\t{user_id}\t\t{time_spent_gaming} sec")
            i += 1
