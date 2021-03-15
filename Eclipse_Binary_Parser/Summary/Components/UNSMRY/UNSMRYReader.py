from Eclipse_Binary_Parser.BaseBinaryWorker.BinaryReader import *


class SPEcBinaryReader(BinaryReader):
    """
    Модернизация BinaryReader для нужд чтения (ускорения) UNSMRY файлов
    """
    def __init__(self, link: str, dimension: tuple):
        super().__init__(link)
        self.loaded = 0
        self.dimension = dimension
        self.results = None

    def _add_data(self, content: Content) -> None:
        if self.results is None:
            value = content.value
            content.value = np.zeros(self.dimension) * np.nan
            content.value[self.loaded, :] = value
            self.results = content
        else:
            value = content.value
            self.results.value[self.loaded, :] = value
        self.loaded += 1


class UNSMRYLoader:
    """
    Загрузчик файлов из UNSMRY файлов
    """
    def __init__(self, link):
        self.link = link

    def get_from_file(self, start: list, length: list,
                      dimension: tuple) -> np.array or list:
        binary_file = SPEcBinaryReader(self.link, dimension)
        binary_file.reading_definite_part('PARAMS', start, length)
        return binary_file.results.value
