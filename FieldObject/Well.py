from FieldObject.InflowZone import *


class Well:
    def __init__(self, name, bounds=None):
        if bounds is None:
            bounds = [0, 2000]
        self.Crutch = Crutch()
        self.name = name
        self.InflowZones = dict()
        self.params = pd.DataFrame()
        self.bounds = bounds


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