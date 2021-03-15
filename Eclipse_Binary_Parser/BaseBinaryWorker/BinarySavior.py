from .Components.Content import *
from .Components.Header import *


def __value_correct(value: list) -> bool:
    return all(list(map(lambda i: type(value[0]) == type(i), value)))


def __definition_datatype(value: list) -> str or None:
    if __value_correct(value):
        if isinstance(value[0], int):
            return 'INTE'
        elif isinstance(value[0], float):
            return 'REAL'
        elif isinstance(value[0], str):
            return 'CHAR'
        elif isinstance(value[0], bool):
            return 'LOGI'
    elif all(list(map(lambda i: isinstance(i, (float, int)), value))):
        return 'REAL'


def create(link):
    with open(link, 'wb') as _:
        pass


def save(link, keyword, value: list):

    number_of_objects = len(value)

    if keyword == 'PARAMS':
        datatype = 'REAL'
    else:
        datatype = __definition_datatype(value)

    header = HeaderConstructor.from_variable(keyword,
                                             number_of_objects,
                                             datatype)
    content = ContentConstructor.from_variable(header, value)
    bytes_content = content.to_bytes()
    with open(link, 'ab+') as file:
        file.write(bytes_content)
