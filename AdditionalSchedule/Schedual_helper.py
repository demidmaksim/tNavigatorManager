from AdditionalSchedule.Bound import *
from scipy.optimize import LinearConstraint
import datetime as dt


class MyLinearConstraint:
    def __init__(self):
        self.__A = []
        self.__lb = []
        self.__ub = []

    def to_scipy(self):
        return LinearConstraint(self.__A, self.__lb, self.__ub)

    def add_bound(self, a: list, lb: float, ub: float):
        self.__A.append(a)
        self.__lb.append(lb)
        self.__ub.append(ub)


def create_linear_constraint():
    return MyLinearConstraint()


def add_object_bound(inflow_zone_order: list,
                     bounds: DebitLimits, now_time: dt,
                     linear_constraint: MyLinearConstraint) \
        -> MyLinearConstraint:

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
                                    bound[DebitLimits.max_vol])

    return linear_constraint


def definition_valve_well(wall_name: str, inflow_zone_order: list):
    valve_in_wells = pd.DataFrame(inflow_zone_order, columns=['Well', 'Valve'])
    valve_pattern = valve_in_wells['Well'] == wall_name
    valve_df = valve_in_wells[valve_pattern]
    valve_in_well = pd.unique(valve_df['Valve'])
    return valve_in_well


def get_border_pattern(obj_name_list: str, inflow_zone_order: list):
    bound = [0 for _ in range(len(inflow_zone_order))]

    for obj_name in obj_name_list:
        valve_in_well = definition_valve_well(obj_name, inflow_zone_order)



        for valve in valve_in_well:
            ind = inflow_zone_order.index([obj_name, valve])
            bound[ind] = 1

    return bound


def add_group_bound(now_time, linear_constraint, bounds, groups,
                    inflow_zone_order):

    bound_objects = list(pd.unique(bounds.df[DebitLimits.well]))
    for obj_id, obj in enumerate(bound_objects):

        if obj not in groups.keys() and obj != 'FIELD':
            patt = bounds.df[DebitLimits.well] == obj
            well = obj
            all_valve_bound = bounds.df[patt][DebitLimits.valve]
            segments = list(pd.unique(all_valve_bound))

            for segment in segments:
                bound = bounds.get_limit(now_time, well, segment)

                if segment != -1 and [well, 1] not in inflow_zone_order:
                    border_pattern = [0] * len(inflow_zone_order)
                    ind = inflow_zone_order.index([well, segment])
                    border_pattern[ind] = 1
                    linear_constraint.add_bound(border_pattern,
                                                bound[DebitLimits.min_vol],
                                                bound[DebitLimits.max_vol])

                elif [well, 1] not in inflow_zone_order:
                    border_pattern = get_border_pattern(well, inflow_zone_order)
                    linear_constraint.add_bound(border_pattern,
                                                bound[DebitLimits.min_vol],
                                                bound[DebitLimits.max_vol])

        elif obj == 'FIELD':
            bound = bounds.get_limit(now_time, 'FIELD', -1)
            border_pattern = [1] * len(inflow_zone_order)
            linear_constraint.add_bound(border_pattern,
                                        bound[DebitLimits.min_vol],
                                        bound[DebitLimits.max_vol])

        elif obj in list(groups.keys()):
            bound = bounds.get_limit(now_time, obj, -1)
            name_groups = list(groups.keys())
            ind = name_groups.index(obj)
            wells_group = groups.iloc[ind, ind]

            for well in wells_group:
                t = get_border_pattern(well, inflow_zone_order)
