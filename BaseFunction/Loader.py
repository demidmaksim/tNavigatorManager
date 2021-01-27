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
                target_function = get_fun(line)
                keyword_data[line] = target_function(list_file)

    return keyword_data


def read_smspec_file(link: str = None):
    # TODO
    link = r'C:\Users\vfrcl\Desktop\Assistant_Simulated\For_Test\Light.SMSPEC'