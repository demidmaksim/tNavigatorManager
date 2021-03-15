from .Components.Time import *


class SMSPECReader:
    """
    Класс для чтения SMSPEC файлов
    Так же в нем в результате храняться данные для чтения из UNSMRY файла
    """
    def __init__(self, link: str):
        self.link = link
        self.storage = None
        self.time = None
        self.dimension = None

    def report(self):
        print('-'*30, 'SMSPEC Report', '-'*30)
        self.storage.report()
        self.time.report()
        print("Dimension\t{}".format(self.dimension))
        print('-' * 75)

    @staticmethod
    def __structuring(for_download: list) -> tuple:
        for_download.sort()
        length = [1]
        start = [for_download[0]]
        for i, point in enumerate(for_download[1:]):
            if point - for_download[i] == 1:
                length[-1] += + 1
            else:
                length.append(1)
                start.append(for_download[i + 1])
        return np.array(start), np.array(length)

    def get_position_matrix(self, names: str or list,
                            keywords: str or list,
                            nums: int or list):
        if type(names) == str or names is None:
            return [names, keywords, nums]
        elif type(names) == list:
            positions_matrix = []
            for name_id, name in enumerate(names):
                keyword = keywords[name_id]

                num = nums[name_id]
                position = self.storage.get_position(name, keyword, num)
                positions_matrix.append([position, name, keyword, num])

            positions_matrix.sort()
            new_position = []
            for position in positions_matrix:
                new_position.append(position[1:])

            return new_position

    def get_read_vector(self, names: str or list,
                        keywords: str or list,
                        nums: int or list) -> tuple:

        if type(names) == str or names is None:
            position = self.storage.get_position(names, keywords, nums)
            return np.array([position]), np.array([1])
        elif type(names) == list:
            positions = []
            for name_id, name in enumerate(names):
                keyword = keywords[name_id]
                num = nums[name_id]
                position = self.storage.get_position(name, keyword, num)
                positions.append(position)
            start, length = self.__structuring(positions)
            return np.array(start), np.array(length)


class SMSPECWorkerConstructor:

    @staticmethod
    def from_file(link: str) -> SMSPECReader:
        smspec = SMSPECReader(link)
        SMSPECWorkerConstructor.__create_storage(smspec)
        SMSPECWorkerConstructor.__create_time(smspec)
        SMSPECWorkerConstructor.__create_dimension(smspec)
        return smspec

    @staticmethod
    def __create_storage(smspec: SMSPECReader) -> None:
        storage = StorageConstructor.from_file(smspec.link)
        smspec.storage = storage

    @staticmethod
    def __create_time(smspec: SMSPECReader) -> None:
        time = TimeConstructor.from_file(smspec.link, smspec.storage)
        smspec.time = time

    @staticmethod
    def __create_dimension(smspec: SMSPECReader) -> tuple:
        number_of_step = len(smspec.time.dey_vector)
        number_of_word = smspec.storage.get_number_of_word()
        smspec.dimension = (number_of_step, number_of_word)
        return number_of_step, number_of_word
