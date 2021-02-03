import numpy as np
from BaseFunction.Crutch import *


class InflowZone:
    def __init__(self, well: str, bore: str,
                 segment: str, device_type: str,
                 fully_open_size: str):
        self.Crutch = Crutch()
        self.well = well
        self.bore = bore
        self.segment = int(segment)
        self.device_type = device_type
        self.fully_open_size = float(fully_open_size)
        self.param = pd.DataFrame()

    def get_param(self, param: str):
        return self.param[param]


class InflowZoneConstructor:
    def __init__(self):
        pass

    @staticmethod
    def create(well: str, bore: str, segment: str, device_type: str,
               fully_open_size: str) -> InflowZone:
        return InflowZone(well, bore, segment, device_type, fully_open_size)

    @staticmethod
    def from_dict(inflowzone_dict) -> InflowZone:
        well = inflowzone_dict['well']
        bore = inflowzone_dict['bore']
        segment = inflowzone_dict['segment']
        device_type = inflowzone_dict['device_type']
        fully_open_size = inflowzone_dict['fully_open_size']
        if fully_open_size == '1*':
            fully_open_size = np.inf
        return InflowZone(well, bore, segment, device_type, fully_open_size)
