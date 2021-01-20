from FieldObject.Well import *
from BaseFunction.Loader import *


class Field:
    def __init__(self, name: str):
        self.name: str = name
        self.wells = dict()

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


class FieldConstructor:

    @staticmethod
    def __create_empty_field(name: str) -> Field:
        return Field(name)

    @staticmethod
    def add_well(field: Field, well: Well):
        field.wells[well.name] = well

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
        return field


field1 = FieldConstructor.create_field()
field1.report()
