import numpy as np
from tNav.For_Debugging import *


class InflowZone:
    """
    Зона притока в скважину. Представляет из себя клапан которым можно управлять
    """
    target_params = {
        "well_params": ['WOPR', 'WWPR', 'WWCT', 'WBHP'],
        'valve_params': ['SOFR', 'SWFR', 'SWCT', 'SPR']
    }

    def __init__(self, well: str, bore: str, segment: str, device_type: str,
                 fully_open_size: str):
        """

        :param well: имя скважины на которой находится клапан
        :param bore: номер/имя ствола
        :param segment: номер сегмента который имитирует клапан
        :param device_type: тип устройства
        :param fully_open_size: максимальный размер клапана для установки
        """

        self.well = well
        self.segm = int(segment)
        self.device_type = device_type
        self.max_size = float(fully_open_size)
        self.param = dict()

    def _set_params(self, param: str, param_data: list or np.array):
        """
        Техническая функция используемая при загрузке данных
        :param param: имя мнимоники
        :param param_data: вектор который необходимо загрузить
        """
        self.param[param] = param_data

    def get_param(self, param: str):

        """
        :param param: имя мнимоники
        :return: Возвращает вектор данных за все расчетные шаги
        """
        param = param.upper()

        if param in self.param.keys():
            return self.param[param]
        else:
            print("The requested parameter is missing!")
            return None

    def get_last_active_param(self, param):
        """
        :param param: имя мнимоники
        :return: Возвращает последнее значение при которой работала скважина
        """
        param = param.upper()

        if param in self.param.keys():
            data = self.param[param]
            for point in reversed(data):
                if point > 0:
                    break
            else:
                point = 0
            return point
        else:
            print("The requested parameter is missing!")
            return None

    def set_valve_size(self, share):
        """
        Управляющее слово секции Schedule
        :param share: Доля от максимального размера клапана
        """
        valve_size = "WSEGVALV\n" \
                     "{} {} 1 {}  /\n" \
                     "/""".format(self.well, self.segm,
                                  self.max_size * share)

        add_keyword(valve_size)


class InflowZoneConstructor:
    """
    Класс конструктор для создания (экземпляров) клапанов
    """
    def __init__(self):
        pass

    @staticmethod
    def create(well: str, bore: str, segment: str, device_type: str,
               fully_open_size: str) -> InflowZone:
        """
        Создает эксземляр клапана
        :param well: имя скважины на которой находится клапан
        :param bore: номер/имя ствола
        :param segment: номер сегмента который имитирует клапан
        :param device_type: тип устройства
        :param fully_open_size: максимальный размер клапана для установки
        """
        return InflowZone(well, bore, segment, device_type, fully_open_size)

    @staticmethod
    def from_dict(inflowzone_dict) -> InflowZone:
        """

        :param inflowzone_dict: словарь загруженый из дополнительного расписния,
        в котором указаны данные для создания зоны притока
        :return:
        """

        well = inflowzone_dict['well']
        bore = inflowzone_dict['bore']
        segment = inflowzone_dict['segment']
        device_type = inflowzone_dict['device_type']
        fully_open_size = inflowzone_dict['fully_open_size']

        if fully_open_size == '1*':
            fully_open_size = np.inf
        return InflowZone(well, bore, segment, device_type, fully_open_size)
