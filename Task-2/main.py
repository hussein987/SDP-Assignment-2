from handle_query import *
from utils import *

import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":

    cloud_gaming = CloudGaming()
    while True:
        command = int(
            input(
                "\nChoose one operation from below :\n\
            1 : Get status for the past 7 days\n\
            2 : Print user summary\n\
            3 : Predict user next session duration\n\
            4 : Fetch new data and update users data and ML model\n\
            5 : Get top 5 users based on time spent gaming\n\
            6 : Exit program\n"
            )
        )
        if command == 1:
            # Get the status for the last 7 days
            cloud_gaming.get_status_of_last_week()
        elif command == 2:
            # Print user summarya
            find_another_user = True
            while find_another_user:
                user_id = input("\nEnter user id:\n")
                time_interval = input("\nEnter period (yy/mm/dd - yy/mm/dd) :\n")
                cloud_gaming.update_query_data(user_id, time_interval.split(' - '))
                cloud_gaming.print_user_summary(save_to_txt=True)
                find_another_user = input("Find another user ? (yes/No)\n")
                find_another_user = (
                    True if find_another_user.lower() == "yes" else False
                )
        elif command == 3:
            # Predict user next session duration
            user_id = input("Enter user id:\n")
            cloud_gaming.update_query_data(user_id)
            print(
                f"\nThe estimated next session time is: {cloud_gaming.predict_next_session_time()}\n"
            )
        elif command == 4:
            # Fetch new data and update users data and ML model
            cloud_gaming.fetch_data()
        elif command == 5:
            # Get top 5 users based on time spent gaming
            cloud_gaming.rank_users_by_gaming_time()
        elif command == 6:
            # Exit
            print("\nStatistics for the past 7 days:\n")
            cloud_gaming.get_status_of_last_week()
            save_summary = input("\nSave summary ? (yes/no)\n")
            if save_summary.lower() == 'yes':
                cloud_gaming.get_status_of_last_week(save_txt=True)
            print("Good bye!!")
            break
