from BaseFunction.ReadHelperFunctions.ASCII import*


def __read_construction(line: list) -> dict:

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

    except IndexError:
        print('Mistake in inflowzo keyword')
        inzo = {
            'well': None,
            'bore': None,
            'segment': None,
            'device_type': None,
            'fully_open_size': None
        }

    return inzo


def __read_bounds(line: list) -> dict:

    try:
        inflow_zones = [None, None]
        for inflow_zone in line[1:-3]:
            if ':' in inflow_zone:
                well = inflow_zone.split(':')[0]
                inflow_zone = inflow_zone.split(':')[1]
            else:
                well = inflow_zone
                inflow_zone = None

            inflow_zones = [well, inflow_zone]

        date = line[0]
        fluid, min_liquid, max_liquid = line[-3], line[-2], line[-1]

        border = {
            'date': date,
            'well': inflow_zones[0],
            'valve/segment': inflow_zones[1],
            'min liquid': min_liquid,
            'max liquid': max_liquid,
            'fluid': fluid
        }

    except IndexError:
        print('Mistake in BOUNDS keyword')
        border = {
            'date': None,
            'well': None,
            'valve/segment': None,
            'min liquid': None,
            'max liquid': None,
            'fluid': None
        }

    return border


def __read_group_list(line: list):

    groups = dict()
    try:
        groups[line[0]] = line[1:]
    except IndexError:
        print('Mistake in BOUNDS keyword')

    maximum = 0
    for key in groups.keys():
        len_dict = len(groups[key])
        if len_dict > maximum:
            maximum = len_dict
    for key in groups.keys():
        add_none = maximum - len(groups[key])
        groups[key].extend([None] * add_none)

    return groups


dict_for_fun = {
    'INFLOWZO': __read_construction,
    'BOUNDS': __read_bounds,
    'MAKEGROUPLIST': __read_group_list
}


def read_keyword(list_file: list, key: str) -> list:
    data = []

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
        target_function = dict_for_fun[key]
        d = target_function(line)
        data.append(d)

    return data
