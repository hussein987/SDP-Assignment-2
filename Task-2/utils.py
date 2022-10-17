import datetime
import io
from contextlib import redirect_stdout


def parse_date(date_string, separator):
    return datetime.datetime.strptime(
        date_string, f"%Y{separator}%m{separator}%d"
    ).date()


def format_time(seconds):
    hours = seconds // 3600
    delta = seconds % 3600
    minutes = delta // 60
    delta = delta % 60
    seconds = delta
    return f"{hours} hrs : {minutes} minutes : {seconds} seconds"


def save_to_file(func):
    def wrapper(*args, **kwd_args):
        if "save_txt" in kwd_args and kwd_args["save_txt"]:
            redirected_out = io.StringIO()
            with redirect_stdout(redirected_out):
                print("Saving the contents to a file")
                func(*args, **kwd_args)
            return redirected_out.getvalue()
        else:
            func(*args, **kwd_args)

    return wrapper
