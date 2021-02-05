from FieldObject.Well import *
from BaseFunction.Loader import *
from FieldObject.Schedule import *
from FieldObject.Field.Field_Assistant import *
from scipy.optimize import Bounds
import numpy as np
from scipy.optimize import LinearConstraint


class Field:
    def __init__(self, name: str):
        self.name: str = name
        self.wells = dict()
        self.bounds: dict or None = None
        self.Schedule = None

    def report(self):
        print(F'Name field: {self.name}')
        for well in self.wells:
            well = self.wells[well]
            print('-'*50)
            print(f'\t Well name: {well.name}')
            for inflowzone in well.InflowZones:
                inflowzone = well.InflowZones[inflowzone]
                print(f'\t|\t inflowzone: {inflowzone.segment}\t'
                      f'Bore: {inflowzone.bore}\t'
                      f'Device Type: {inflowzone.device_type}')
        print('-'*50)
        '''
        if self.bounds:
            for bound in self.bounds:
                inflow_zones = bound['inflow zones']
                data_for_report = []
                for inflow_zone in inflow_zones:
                    if inflow_zone[1]:
                        data_for_report.append(f'{inflow_zone[0]}:'
                                               f'{inflow_zone[1]}')
                    else:
                        data_for_report.append(f'{inflow_zone[0]}')

                for_report = ' + '.join(data_for_report)
                print(f'bound: {bound["fluid"]}\t'
                      f'{bound["min liquid"]} < '
                      f'{for_report}'
                      f' > {bound["max liquid"]}')
        '''

        print('-'*30)
        print(self.Schedule.bounds)

        print('-'*30)
        print(self.Schedule.groups)

    def get_pattern(self) -> list:
        pattern = []
        wells = list(self.wells.keys())
        wells.sort()

        for well_name in wells:
            inflow_zones = self.wells[well_name].InflowZones.keys()
            inflow_zones.sort()
            for inflow_zone in inflow_zones:
                pattern.append([well_name, inflow_zone])

        return pattern

    def get_bounds(self):
        pass


class FieldConstructor:

    @staticmethod
    def __create_empty_field(name: str) -> Field:
        return Field(name)

    @staticmethod
    def add_well(field: Field, well: Well):
        field.wells[well.name] = well

    @staticmethod
    def add_schedule(field: Field, additional_data: dict):
        schedule = ScheduleConstructor.create_schedule(additional_data)
        field.Schedule = schedule

    @staticmethod
    def add_inflowzone(field: Field, inflowzone: InflowZone):
        if inflowzone.well not in field.wells:
            well = WellConstructor.create_well(inflowzone.well)
            WellConstructor.add_zone(well, inflowzone)
            FieldConstructor.add_well(field, well)
        else:
            well = field.wells[inflowzone.well]
            WellConstructor.add_zone(well, inflowzone)

    @staticmethod
    def create_field() -> Field:
        field = FieldConstructor.__create_empty_field('name')
        additional_data = read_additional_schedule()

        for inflowzone in additional_data['INFLOWZO']:
            inflowzone = InflowZoneConstructor.from_dict(inflowzone)
            FieldConstructor.add_inflowzone(field, inflowzone)

        FieldConstructor.add_schedule(field, additional_data)

        return field

    @staticmethod
    def create_test_field(self) -> Field:
        field = FieldConstructor.create_field()

        return field