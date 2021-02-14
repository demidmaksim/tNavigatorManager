from BaseFunction.ReadHelperFunctions.KeyWordSet import *
from BaseFunction.Crutch import *


def read_additional_schedule() -> dict:
    addit_sch = get_additional_schedule_link()
    keyword_data = dict()
    with open(addit_sch, 'r') as file:
        list_file = file.read().split('\n')

        while list_file:
            line = clean_from_comment(list_file.pop(0))

            if this_is_skip(line):
                pass

            elif this_is_keyword(line):
                keyword_data[line] = read_keyword(list_file, line)

    return keyword_data
