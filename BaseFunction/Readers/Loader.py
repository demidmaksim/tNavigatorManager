from BaseFunction.Readers.ReadHelperFunctions.KeyWordSet import *
from tNav.For_Debugging import *

__additional_schedule_name = 'Additional Schedule.INC'


def get_additional_schedule_link() -> str:
    """
    :return: ссылку на файл Additional Schedule.INC
    """
    folder = get_project_folder().replace('/', '\\') + '\\'
    return folder + __additional_schedule_name


def read_additional_schedule() -> dict:
    """
    Чтение файла Additional Schedule.INC
    :return: словарь с разделением по ключевым словам данных прочитанных в файле
    """
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
