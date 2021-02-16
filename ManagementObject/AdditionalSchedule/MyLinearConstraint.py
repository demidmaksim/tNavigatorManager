from ManagementObject.AdditionalSchedule.Bound import *
from scipy.optimize import LinearConstraint
import datetime as dt
import numpy as np


class MyLinearConstraint:
    def __init__(self):
        self.__A = []
        self.__lb = []
        self.__ub = []
        self.__fluid_type = []

    def to_scipy(self):
        return LinearConstraint(self.__A, self.__lb, self.__ub)

    def add_bound(self, a: list, lb: float, ub: float, __fluid_type: str):
        self.__A.append(a)
        self.__lb.append(lb)
        self.__ub.append(ub)
        self.__fluid_type.append(__fluid_type)

    def calculate_water_cut(self, water_cut: np.array):
        self.__A = np.array(self.__A, dtype=float)
        for line_id, line in enumerate(self.__fluid_type):
            if line == 'OIL':
                self.__A[line_id, :] = self.__A[line_id, :] * (1 - water_cut)
            elif line == 'WATER':
                self.__A[line_id, :] = self.__A[line_id, :] * water_cut

    def get_report(self):
        print(f'len: {len(self.__lb)}\tlc.lb: {self.__lb}')
        print(f'len: {len(self.__ub)}\tlc.ub: {self.__ub}')
        print(f'len: {len(self.__fluid_type)}\nlc.A:'
              f' {np.array(self.__fluid_type)}')
        print(f'len: {len(self.__A)}\nlc.A: {np.array(self.__A)}')


def create_linear_constraint():
    return MyLinearConstraint()


def definition_valve_well(wall_name: str, inflow_zone_order: list):
    valve_in_wells = pd.DataFrame(inflow_zone_order, columns=['Well', 'Valve'])
    valve_pattern = valve_in_wells['Well'] == wall_name
    valve_df = valve_in_wells[valve_pattern]
    valve_in_well = pd.unique(valve_df['Valve'])
    return list(valve_in_well)


def get_border_pattern(wells: list, inflow_zone_order: list) -> list:
    border_pattern = [0 for _ in range(len(inflow_zone_order))]

    for well in wells:
        well_valves = definition_valve_well(well, inflow_zone_order)
        for valve in well_valves:
            ind = inflow_zone_order.index([well, valve])
            border_pattern[ind] = 1

    return list(border_pattern)


def __add_object_bound(inflow_zone_order: list,
                       bounds: DebitLimits, now_time: dt,
                       linear_constraint: MyLinearConstraint) -> None:
    for obj_id, well in enumerate(inflow_zone_order):
        if well[1] != 1:
            well, segment = well[0], well[1]
        else:
            well, segment = well[0], -1

        bound = bounds.get_limit(now_time, well, segment)

        border_pattern = [0] * len(inflow_zone_order)
        border_pattern[obj_id] = 1

        linear_constraint.add_bound(border_pattern,
                                    bound[DebitLimits.min_vol],
                                    bound[DebitLimits.max_vol],
                                    bound[DebitLimits.fluid])


def __add_well_bound(linear_constraint, now_time, bounds,
                     well, inflow_zone_order) -> None:

    all_valve = definition_valve_well(well, inflow_zone_order)

    if len(all_valve) != 1:
        border_pattern = get_border_pattern([well], inflow_zone_order)
        bound = bounds.get_limit(now_time, well, -1)
        linear_constraint.add_bound(border_pattern,
                                    bound[DebitLimits.min_vol],
                                    bound[DebitLimits.max_vol],
                                    bound[DebitLimits.fluid])


def __add_field_bound(constraint: MyLinearConstraint,
                      time: dt, bounds: DebitLimits,
                      inflow_zone_order: list) -> None:

    bound = bounds.get_limit(time, 'FIELD', -1)
    border_pattern = [1] * len(inflow_zone_order)
    constraint.add_bound(border_pattern,
                         bound[DebitLimits.min_vol],
                         bound[DebitLimits.max_vol],
                         bound[DebitLimits.fluid])


def __add_group_bound(constraint: MyLinearConstraint, time: dt,
                      bounds: DebitLimits, well_list, group_name: str,
                      inflow_zone_order: list) -> None:

    bound = bounds.get_limit(time, group_name, -1)
    border_pattern = get_border_pattern(well_list, inflow_zone_order)

    constraint.add_bound(border_pattern,
                         bound[DebitLimits.min_vol],
                         bound[DebitLimits.max_vol],
                         bound[DebitLimits.fluid])


def add_bound(time: dt, constraint: MyLinearConstraint,
              bounds: DebitLimits, groups: dict, infl_zone_order: list) -> None:
    __add_object_bound(infl_zone_order, bounds, time, constraint)

    bound_groups = list(pd.unique(bounds.df[DebitLimits.well]))
    for group_id, group in enumerate(bound_groups):

        if group not in list(groups.keys()) and group != 'FIELD':
            well = group
            __add_well_bound(constraint, time, bounds, well, infl_zone_order)

        elif group == 'FIELD':
            __add_field_bound(constraint, time, bounds, infl_zone_order)

        elif group in list(groups.keys()):
            __add_group_bound(constraint, time, bounds,
                              groups[group], group, infl_zone_order)
