from BaseFunction.ReadHelperFunctions.ASCII import*
import pandas as pd
import datetime as dt


def __read_construction(list_file: list) -> list:

    field_object = list()

    while list_file:

        line = list_file.pop(0)
        while this_is_skip(line) and list_file:
            line = list_file.pop(0)

        if not list_file:
            break

        line = clean_from_comment(line)

        if this_is_end_keyword(line):
            break

        line = line.split()
        try:
            well, bore, segment = line[0], line[1], line[2]
            dev_type, max_size = line[3], line[4]

            inzo = {
                'well': well,
                'bore': bore,
                'segment': segment,
                'device_type': dev_type,
                'fully_open_size': max_size
            }
            field_object.append(inzo)

        except BaseException:
            print('Mistake in inflowzo keyword')

    return field_object


def __read_bounds(list_file):

    bounds_list = []

    while list_file:

        line = list_file.pop(0)

        while this_is_skip(line) and list_file:
            line = list_file.pop(0)

        if not list_file:
            break

        line = clean_from_comment(line)

        if this_is_end_keyword(line):
            break

        line = clean_from_comment(line)

        if this_is_end_keyword(line):
            break

        line = line.split()

        try:
            inflow_zones = []

            for inflow_zone in line[1:-3]:
                if ':' in inflow_zone:
                    well = inflow_zone.split(':')[0]
                    inflow_zone = inflow_zone.split(':')[1]
                else:
                    well = inflow_zone
                    inflow_zone = None

                inflow_zones.append([well, inflow_zone])

            data = line[1]
            fluid, min_liquid, max_liquid = line[-3], line[-2], line[-1]

            border = {
                'inflow zones': inflow_zones,
                'min liquid': min_liquid,
                'max liquid': max_liquid,
                'fluid': fluid,

            }

            bounds_list.append(border)

        except BaseException:
            print('Mistake in inflowzo keyword')

    return bounds_list


dict_for_fun = {
    'INFLOWZO': __read_construction,
    'BOUNDS': __read_bounds
}


def get_fun(key: str) -> callable or None:
    if key in dict_for_fun:
        return dict_for_fun.get(key)
    else:
        print('Тo such keyword!')
