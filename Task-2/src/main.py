from handle_query import *
from utils import *

if __name__ == "__main__":

    cloud_gaming = CloudGaming(1, 0)


    # get_date = lambda datetime_str: datetime.datetime.strptime(datetime_str, f"%Y-%m-%d %H:%M:%S")
    # first_session = get_date(user_df.iloc[0]["timestamp"])
    
    # avg = 0 
    # for session in sessions:
    #     get_date = lambda datetime_str: datetime.datetime.strptime(datetime_str, f"%Y-%m-%d %H:%M:%S")
    #     first_session = get_date(user_df[user_df["session_id"] == session].iloc[0]["timestamp"])
    #     last_session = get_date(user_df[user_df["session_id"] == session].iloc[-1]["timestamp"])
    #     diff = last_session - first_session
    #     avg += diff.seconds
    #     print(format_time(diff.seconds))
    # print(avg // len(sessions))
    # print(format_time(avg // len(sessions)))

    # GET THE SPENT ON A SESSION
    # datetime_str = fetched_data[fetched_data['client_user_id'] == '052f1085-d37f-41c3-b003-5e7a2c64f075'].iloc[0]['timestamp']
    # start_time = datetime.datetime.strptime(datetime_str, f"%Y-%m-%d %H:%M:%S")

    # datetime_str = fetched_data[fetched_data['client_user_id'] == '052f1085-d37f-41c3-b003-5e7a2c64f075'].iloc[1]['timestamp']
    # end_time = datetime.datetime.strptime(datetime_str, f"%Y-%m-%d %H:%M:%S")

    # delta = end_time - start_time
    # hours = delta.seconds // 3600
    # delta = delta.seconds % 3600
    # minutes = delta // 60
    # delta = delta % 60
    # seconds = delta
    # print(f"{hours} hrs : {minutes} minutes : {seconds} seconds")

    # print(fetched_data.groupby(['client_user_id']).mean())

    while True:
        command = int(
            input(
                "Choose one operation from below :\n\
            1 : Get status for the past 7 days\n\
            2 : Print user summary\n\
            3 : Predict user next session duration\n\
            4 : Fetch new data and update users data and ML model\n\
            5 : Get top 5 users based on time spent gaming\n\
            6 : Exit program\n"
            )
        )
        if command == 1:
            cloud_gaming.fetch_data(3)
        # elif command == 2:
        #     add_room(universities)
        # elif command == 3:
        #     print_institution(universities)
        # elif command == 4:
        #     assign_activity(universities, "Classroom")
        # elif command == 5:
        #     assign_activity(universities, "Auditorium")
        # elif command == 6:
