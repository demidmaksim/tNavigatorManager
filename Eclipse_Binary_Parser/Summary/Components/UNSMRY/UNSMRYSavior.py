from Eclipse_Binary_Parser.BaseBinaryWorker.BinarySavior import *

"""
Раздел для записи данных в UNSMRY файлов
"""


def create_unsmry(link):
    with open(link, 'wb') as _:
        pass


def add_in_unsmry_file(link, value):
    save(link, 'PARAMS', value)
