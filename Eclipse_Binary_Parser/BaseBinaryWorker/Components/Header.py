from struct import unpack, pack
from typing import BinaryIO
import numpy as np


class Header:
    """
    класс с данными о заголовке в бинарных файлах, после которых идет информация
    Содержит длинну области размер, одного слова, тип переменных
    """
    length_header = 24  # 24 is size of header
    significant_byte = 16  # 16 is size significant byte area of header

    def __init__(self, keyword: str, number_of_objects: int, datatype: str):
        self.keyword = keyword
        self.number_of_objects = number_of_objects
        self.datatype = datatype
        self.length = None
        self.format = None
        self.start_reading = None
        self.len_reading = None

    def __eq__(self, other):
        if self.keyword == other.keyword:
            return True
        else:
            return False

    @staticmethod
    def __supplement(word: str, must_length: int) -> str:
        if len(word) < must_length:
            supplement = must_length - len(word)
            return word + ' ' * supplement
        elif len(word) >= must_length:
            return word[:must_length]

    def set_limitation(self, start_reading: np.array, len_reading: np.array):
        self.start_reading = start_reading * self.length
        self.len_reading = len_reading * self.length

    def to_byte(self) -> bytes:
        bytes_list = [
            pack('>i', self.significant_byte),
            self.__supplement(self.keyword, 8).encode('utf-8'),
            pack('>i', self.number_of_objects),
            self.__supplement(self.datatype, 4).encode('utf-8'),
            pack('>i', self.significant_byte)
        ]
        return b''.join(bytes_list)

    def get_length_target_bytes(self):
        return self.length * self.number_of_objects

    def get_ending(self):
        if self.start_reading is not None and self.len_reading is not None:
            return self.start_reading + self.len_reading
        else:
            return None


class HeaderConstructor:
    datatype = {'INTE': {'length': 4, 'format': 'i'},
                'LOGI': {'length': 4, 'format': '?'},
                'REAL': {'length': 4, 'format': 'f'},
                'CHAR': {'length': 8, 'format': 'c'},
                'DOUB': {'length': 8, 'format': 'd'}}

    def __byte_init(self, header: Header) -> Header:
        if header.datatype in HeaderConstructor.datatype.keys():
            header.length = self.datatype[header.datatype]['length']
            header.format = self.datatype[header.datatype]['format']
        elif header.datatype[:2] == 'C0':
            header.length = int(header.datatype[2:])
            header.format = 'c'
        else:
            pass
        return header

    def from_bytes(self, binary_info: bytes) -> Header:
        header = Header(
            str(binary_info[4:12], 'utf-8').strip(),
            unpack('>i', binary_info[12:16])[0],
            str(binary_info[16:20], 'utf-8')
        )
        return self.__byte_init(header)

    @staticmethod
    def from_variable(keyword: str, number_of_objects: int,
                      datatype: str) -> Header:
        header = Header(keyword, number_of_objects, datatype)
        hc = HeaderConstructor()
        return hc.__byte_init(header)

    def from_file(self, file: BinaryIO):
        binary_header = file.read(Header.length_header)
        return self.from_bytes(binary_header)
