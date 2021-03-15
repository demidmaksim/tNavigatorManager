import os
import datetime as dt

__additional_schedule_name = 'Additional Schedule.INC'


def get_project_folder():
    # это симулирует работу тНава
    return os.getcwd()


def get_additional_schedule_link() -> str:
    folder = get_project_folder().replace('/', '\\') + '\\'
    return folder + __additional_schedule_name


def get_smspec_key_word():
    link = os.getcwd() + '\\Eclipse_Binary_Parser\\Summary\\Components\\SMSPEC'
    return link + '\\keyword.txt'


def get_current_date():
    return dt.datetime(2023, 1, 1)


def add_keyword(control_word: str):
    print(control_word)
