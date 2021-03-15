from .Header import *
import numpy as np


class Content:
    """
    Класс данными бинарных файлов, содержит как заголовок так и данные
    """
    determinant = 4  # 4 is size of zone(area) length determinant

    def __init__(self, header, value):
        self.header = header
        self.value = value

    def __eq__(self, other):
        if self.header.keyword == other.header.keyword:
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

    def get_length_target_bytes(self) -> int:
        return self.header.length * self.header.number_of_objects

    def get_content(self) -> list or np.array or None:
        return self.value

    def value_to_bytes(self) -> bytes:
        if self.header.format in ['i', 'f']:
            content = []
            for point in self.value:
                content.append(pack('>' + self.header.format, point))
            byte_content = b''.join(content)
        elif self.header.format == 'c':
            content = []
            for point_id, point in enumerate(self.value):
                content.append(self.__supplement(point, self.header.length))
            byte_content = ''.join(content).encode('utf-8')
        else:
            byte_content = b''
        title = pack('>i', len(byte_content))
        return title + byte_content + title

    def to_bytes(self) -> bytes:
        byte_header = self.header.to_byte()
        byte_content = self.value_to_bytes()
        return byte_header + byte_content

    def add_simple_value(self, value: list or tuple) -> None:
        if type(self.value[0]) == list or type(self.value[0]) == tuple:
            self.value.append(value)
        else:
            self.value = [self.value[:]]
            self.value.append(value)
            
    def add_unsmry_value(self, value) -> None:
        if type(self.value[0]) == list or type(self.value[0]) == tuple:
            self.value.append(value)
        else:
            self.value = [self.value[:]]


class ContentConstructor:

    @staticmethod
    def convert(header: Header, binary_info: bytes) -> tuple or list:
        dtype = header.format
        lenformat = header.length
        number = int(len(binary_info)/lenformat)

        if header.format != 'c':
            value = unpack('>' + dtype * number, binary_info)
        else:
            text = str(binary_info, 'utf-8')
            size = header.length
            numb = int(len(text) / header.length)
            value = [text[i * size:(i + 1) * size].strip() for i in range(numb)]
        return value

    @staticmethod
    def get_byte_area(file: BinaryIO, header: Header) -> bytes:
        read = 0
        bytes_list = []
        while read < header.get_length_target_bytes():
            size_area = unpack('>i', file.read(Content.determinant))[0]
            bytes_list.append(file.read(size_area))
            file.seek(Content.determinant, 1)
            read += size_area
        return b''.join(bytes_list)

    def read_definite_part(self, header: Header, file: BinaryIO) -> Content:
        bytedata = self.get_byte_area(file, header)
        bytes_list = []
        ending = header.get_ending()
        for start_id, start in enumerate(header.start_reading):
            if ending[start_id] < len(bytedata):
                bytes_list.append(bytedata[start:ending[start_id]])
            else:
                bytes_list.append(bytedata[start:ending[start_id]])
                break
        content = Content(header, None)
        content.value = self.convert(header, b''.join(bytes_list))
        return content

    def read_all_block(self, header: Header, file: BinaryIO) -> Content:
        content = Content(header, None)
        bytedata = self.get_byte_area(file, header)
        content.value = self.convert(header, bytedata)
        return content

    @staticmethod
    def skip_all_block(header: Header, file: BinaryIO) -> None:
        read = 0
        while read < header.get_length_target_bytes():
            size_area = unpack('>i', file.read(Content.determinant))[0]
            file.seek(size_area + Content.determinant, 1)
            read += size_area

    @staticmethod
    def from_variable(header: Header,
                      value: list) -> Content:
        content = Content(header, value)
        content.star_block = None
        return content

    def from_file(self, header: Header,
                  file: BinaryIO,  mode: str) -> Content or None:

        if mode == 'all':
            return self.read_all_block(header, file)

        elif mode == 'definite' and header.start_reading is not None:
            return self.read_definite_part(header, file)
