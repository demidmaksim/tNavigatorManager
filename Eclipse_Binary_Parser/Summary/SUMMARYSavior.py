from .Components.SMSPEC.SMSPECSavior import *
from .Components.UNSMRY.UNSMRYSavior import *


"""
Функии для записи данных с расчтных шагов в бинарные файлы
"""


def create_summary(link, kwords, names, nums, units, start_date):
    create_smspec(link, kwords, names, nums, units, start_date)
    create_unsmry(link.replace('SMSPEC', 'UNSMRY'))


def write_summary(link, value):
    add_in_unsmry_file(link.replace('SMSPEC', 'UNSMRY'), value)

