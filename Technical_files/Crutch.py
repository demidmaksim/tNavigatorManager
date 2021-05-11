import os
import pandas as pd
import datetime as dt

__additional_schedule_name = 'Additional Schedule.INC'


def get_project_folder():
    return os.getcwd()


def get_additional_schedule_link() -> str:
    folder = get_project_folder().replace('/', '\\') + '\\'
    return folder + __additional_schedule_name

