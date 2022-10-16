import datetime

def parse_date(date_string, separator):
    return datetime.datetime.strptime(date_string, f"%Y{separator}%m{separator}%d").date()

def format_time(seconds):
    hours = seconds // 3600
    delta = seconds % 3600
    minutes = delta // 60
    delta = delta % 60
    seconds = delta
    return f"{hours} hrs : {minutes} minutes : {seconds} seconds"