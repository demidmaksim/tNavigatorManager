from ManagementObject.InflowZone import *
from typing import Dict
import pandas as pd


class Well:
    def __init__(self, name, bounds=None):
        if bounds is None:
            bounds = [0, 2000]

        self.name: str = name
        self.InflowZones: Dict[int, InflowZone] = dict()
        self.params = pd.DataFrame()
        self.bounds = bounds

    def get_param(self, param: str, inflow_zones: int or None = None):
        if inflow_zones:
            return self.params[param]
        else:
            return self.InflowZones[inflow_zones].get_param(param)


class WellConstructor:
    def __init__(self):
        pass

    @staticmethod
    def add_zone(well: Well,  inflow_zone: InflowZone) -> None:
        well.InflowZones[inflow_zone.segment] = inflow_zone

    @staticmethod
    def create_well(name: str, inflow_zones: list or None = None,
                    bounds=None) -> Well:
        well = Well(name, bounds)
        if inflow_zones is not None:
            for inflow_zone in inflow_zones:
                WellConstructor.add_zone(well, inflow_zone)
        return well

    def add_info(self, df: pd.DataFrame) -> None:
        pass
