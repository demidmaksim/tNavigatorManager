from ManagementObject.Well import *
from BaseFunction.Readers.Loader import *
from ManagementObject.AdditionalSchedule.Schedule import *
from Eclipse_Binary_Parser.Summary.SUMMARYReader import SUMMARYReader
import time


class Field:
    def __init__(self, name: str):
        self.name: str = name
        self.wells: Dict[str, Well] = dict()
        self.bounds: DebitLimits or None = None
        self.Schedule: Schedule or None = None

    def get_pattern(self) -> list:
        pattern = []
        wells = list(self.wells.keys())
        wells.sort()

        for well_name in wells:
            inflow_zones = list(self.wells[well_name].InflowZones.keys())
            inflow_zones.sort()
            for inflow_zone in inflow_zones:
                pattern.append([well_name, inflow_zone])

        return pattern

    def get_inflow_zone(self):
        pattern = self.get_pattern()
        for field_object in pattern:
            well_name = field_object[0]
            segment = field_object[1]
            yield self.wells[well_name].InflowZones[segment]

    def get_params(self, pattern: list, param: str) -> list:
        params_list = []

        for object_id in pattern:
            well = object_id[0]
            inflow_zones = object_id[1]
            param = self.wells[well].get_param(param, inflow_zones)
            params_list.append(param)

        return params_list

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

        self.Schedule.report()


class FieldConstructor:

    @staticmethod
    def __create_empty_field(name: str) -> Field:
        return Field(name)

    @staticmethod
    def __add_well(field: Field, well: Well):
        field.wells[well.name] = well

    @staticmethod
    def __add_schedule(field: Field, additional_data: dict):
        schedule = ScheduleConstructor.create_schedule(additional_data)
        field.Schedule = schedule

    @staticmethod
    def __add_inflowzone(field: Field, inflowzone: InflowZone):
        if inflowzone.well not in field.wells:
            well = WellConstructor.create_well(inflowzone.well)
            WellConstructor.add_zone(well, inflowzone)
            FieldConstructor.__add_well(field, well)
        else:
            well = field.wells[inflowzone.well]
            WellConstructor.add_zone(well, inflowzone)

    @staticmethod
    def __read_additional_schedule(field):
        additional_data = read_additional_schedule()

        for inflowzone in additional_data['INFLOWZO']:
            inflowzone = InflowZoneConstructor.from_dict(inflowzone)
            FieldConstructor.__add_inflowzone(field, inflowzone)

        FieldConstructor.__add_schedule(field, additional_data)

    @staticmethod
    def __read_summary_file(field: Field):
        t = time.time()
        smspec = SUMMARYReader('tNavigatorManager.SMSPEC')
        target_params = {
            "well_params": ['WOPR', 'WWPR'],
            'valve_params': ['SOFR', 'SWFR']
        }

        wells = []
        main_params = []
        nums = []

        for inflow_zone in field.get_inflow_zone():
            well = inflow_zone.well
            segment = inflow_zone.segment
            if segment == 1:
                for param_id, param in enumerate(target_params['well_params']):
                    wells.append(well)
                    main_params.append(param)
                    nums.append(None)
            else:
                for param in target_params['valve_params']:
                    wells.append(well)
                    main_params.append(param)
                    nums.append(segment)

        data_params = smspec.get(wells, main_params, nums)
        positions = smspec.get_position_matrix(wells, main_params, nums)

        for inflow_zone in field.get_inflow_zone():
            well = inflow_zone.well
            segment = inflow_zone.segment
            if segment == 1:
                params = target_params['valve_params']
                for param_id, param in enumerate(target_params["well_params"]):
                    target = [well, param, None]
                    ind = positions.index(target)
                    inflow_zone.set_params(params[param_id], data_params[:, ind])
                    # print(f'param:  {params[param_id]}\t len:  {len(data_params[:, ind])}\n{data_params[:, ind]}')
            else:
                for param in target_params['valve_params']:
                    target = [well, param, segment]
                    ind = positions.index(target)
                    inflow_zone.set_params(param, data_params[:, ind])
                    # print(f'param:  {param}\tlen:  {len(data_params[:, ind])}\n{data_params[:, ind]}')

        print(f'DownLoad Time: {round(time.time() - t, 3)}')

        for inflow_zone in field.get_inflow_zone():
            well = inflow_zone.well
            segment = inflow_zone.segment
            if segment == 1:
                params = ['SOFR', 'SWFR']
                for param_id, param in enumerate(['WOPR', 'WWPR']):
                    param_data = smspec.get(well, param, None)
                    inflow_zone.set_params(params[param_id], param_data)
            else:
                for param in ['SOFR', 'SWFR']:
                    param_data = smspec.get(well, param, segment)
                    inflow_zone.set_params(param, param_data)
        print(f'DownLoad Time: {round(time.time() - t, 3)}')

    @staticmethod
    def create_field() -> Field:
        field = FieldConstructor.__create_empty_field('name')
        FieldConstructor.__read_additional_schedule(field)
        FieldConstructor.__read_summary_file(field)
        return field

    @staticmethod
    def create_test_field() -> Field:
        field = FieldConstructor.create_field()

        return field
