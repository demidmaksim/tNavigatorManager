import os
from .Components.Content import *


class BinaryReader:
    #  Универсальный класс для чтения любых бинарных файлов формата eclipse

    def __init__(self, link: str):
        self.link = link
        self.data = dict()
        self.__HeadConst = HeaderConstructor()
        self.__ContConst = ContentConstructor()

    def report(self):
        """
        Отчет о прачитанных данных
        """
        for key in self.data.keys():
            print('Key: {}'.format(key))
            if type(self.data[key]) == Content:
                print('\t{}'.format(self.data[key].value[:100]))
            else:
                print('\t{}'.format(self.data[key]))

    def _add_data(self, content: Content) -> None:
        """
        добавляет в славарь прочитанные данные в соответсвующий экземлпяр класса
        контент или же создает ноый
        :param content: экземлпяр класса контент для записи
        """
        if content.header.keyword in self.data.keys():
            self.data[content.header.keyword].add_simple_value(content.value)
        else:
            self.data[content.header.keyword] = content

    def reload_data(self) -> None:
        """
        Удаляет загруженные данные
        """
        self.data = dict()

    def reading_all_file(self) -> None:
        """
        Читает весь файл
        """
        self.reload_data()
        with open(self.link, 'rb') as file:
            while file.tell() < os.path.getsize(self.link):
                header = self.__HeadConst.from_file(file)
                content = self.__ContConst.from_file(header, file, mode='all')
                self._add_data(content)

    def reading_definite_part(self, keyword: str,
                              start_reading: np.array,
                              len_reading: np.array) -> None:
        """
        Читает заданные позиции из заданного ключевого слова.
         Значительно сокращает время и объем памяти для загрузки информации из
          бинарных файлов по сравнению с последовательной полной загрузкой и
          получением срезов из листо/массивов
        :param keyword: ключевое слово из которого нееобходимо прочитать данные
        :param start_reading: лист с позициями внутри ключевого слова для старта
         чтения
        :param len_reading: лист с количеством слов, которое необходимо
         прочитать при соответсвующем старте

        """

        self.reload_data()
        with open(self.link, 'rb') as file:

            while file.tell() < os.path.getsize(self.link):
                header = self.__HeadConst.from_file(file)
                header.set_limitation(start_reading, len_reading)
                if keyword == header.keyword:
                    content = self.__ContConst.from_file(header, file,
                                                         mode='definite')
                    self._add_data(content)
                else:
                    self.__ContConst.skip_all_block(header, file)
