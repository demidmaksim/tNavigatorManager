from BaseFunction.ReadHelperFunctions.ASCII import*


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


dict_for_fun = {
    'INFLOWZO': __read_construction
}


def get_fun(key: str) -> callable or None:
    if key in dict_for_fun:
        return dict_for_fun.get(key)
    else:
        print('Тo such keyword!')
