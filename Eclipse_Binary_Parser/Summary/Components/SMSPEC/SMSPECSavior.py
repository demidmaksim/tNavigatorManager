from Eclipse_Binary_Parser.BaseBinaryWorker.BinarySavior import *
from tNav.For_Debugging import *
import pandas as pd

"""
Функции для записи в SMSPEC файлы
"""


def create_keyword_vectors(well_names, well_params,
                           well_segments, segment_names, segment_params):
    link = get_smspec_key_word()
    units_df = pd.read_csv(link, sep='\t')
    kwords = ['TIME']
    names = [':+:+:+:+']
    units = ['DAYS']
    nums = [0]

    for param in well_params:
        for well in well_names:
            unit = units_df[units_df['Keyword'] == param]['Unit'].values[0]
            kwords.append(param)
            names.append(well)
            nums.append(0)
            units.append(unit)

    for param in segment_params:
        for w_id, well in enumerate(well_segments):
            segment = segment_names[w_id]
            unit = units_df[units_df['Keyword'] == param]['Unit'].values[0]
            kwords.append(param)
            names.append(well)
            nums.append(segment)
            units.append(unit)

    return kwords, names, nums, units


def create_smspec(link, kwords, names, nums, units, start_date):
    create(link)
    save(link, 'STARTDAT', start_date)
    save(link, 'KEYWORDS', kwords)
    save(link, 'WGNAMES', names)
    save(link, 'NUMS', nums)
    save(link, 'UNITS', units)


def add_in_smspec_file(link, keyword, value):
    save(link, keyword, value)
