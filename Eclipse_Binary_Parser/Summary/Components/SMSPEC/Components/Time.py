import datetime as dt
from .Storage import *


class Time:
    """
    класс для хранения и обработки вреиенных шагов
    """
    def __init__(self, start_date, dey_vector, dt_vector):
        self.start_date = start_date
        self.dey_vector = dey_vector
        self.dt_vector = dt_vector

    def get_number_of_step(self) -> int:
        return len(self.dey_vector)

    def report(self):
        print("Start date:\t{}".format(self.start_date))
        print('End date:\t{}'.format(self.dt_vector[-1]))
        print('Number of step:\t{}'.format(self.get_number_of_step()))


class TimeConstructor:
    """
    Класс для создания экземляра класса TIME. Производит чтение из UNSMRY,
     SMSPEC файлов и конвертирует в datatime
    """
    @staticmethod
    def from_file(link: str, storage: Storage) -> Time:

        start_date = TimeConstructor.__get_start_time(link)
        dey_vector = TimeConstructor.__get_time_vec(link, storage)
        dt_vector = TimeConstructor.__conv_to_datetime(start_date, dey_vector)
        return Time(start_date, dey_vector, dt_vector)

    @staticmethod
    def __get_datetime(start_date: dt.datetime, days: float) -> dt.datetime:
        return start_date + dt.timedelta(days=float(days))

    @staticmethod
    def __conv_to_datetime(start_date: dt.datetime,
                           dey_vect: list or np.ndarray) -> list:
        return [TimeConstructor.__get_datetime(start_date, i) for i in dey_vect]

    @staticmethod
    def __get_start_time(link: str) -> dt.datetime:
        binary_file = BinaryReader(link)
        binary_file.reading_all_file()
        start_date = binary_file.data['STARTDAT'].value
        day = start_date[0]
        month = start_date[1]
        year = start_date[2]
        hour = start_date[3]
        minute = start_date[4]
        second = int(start_date[5])
        start_date = dt.datetime(year, month, day, hour, minute, second)
        return start_date

    @staticmethod
    def __get_time_vec(link: str, storage: Storage) -> np.ndarray:
        unsmry_link = link.replace('SMSPEC', 'UNSMRY')
        unsmry = BinaryReader(unsmry_link)
        start = storage.get_time_position('TIME')
        unsmry.reading_definite_part('PARAMS', np.array(start), np.array([1]))
        time_model = np.array(unsmry.data['PARAMS'].value)

        time_model = time_model.T

        if type(time_model[0]) == list or type(time_model[0]) == np.ndarray:
            time_model = time_model[0]

        return time_model
