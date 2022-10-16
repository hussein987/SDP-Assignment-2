import datetime

def parse_date(date_string, separator):
    return datetime.datetime.strptime(date_string, f"%Y{separator}%m{separator}%d").date()