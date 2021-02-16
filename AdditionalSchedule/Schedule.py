import datetime as dt
from AdditionalSchedule.Schedual_helper import *


class Schedule:
    def __init__(self):
        self.bounds = None
        self.groups = None

    def get_current_boundaries(self, now_time: dt, inflow_zone_order: list):
        my_linear_constraint = create_linear_constraint()
        add_bound(now_time, my_linear_constraint, self.bounds,
                  self.groups, inflow_zone_order)
        return my_linear_constraint

    def report(self):

        if self.groups is not None:
            print('-' * 30)
            print(self.groups)

        if self.bounds is not None:
            print(self.bounds.df)
            print('-' * 30)


class ScheduleConstructor:

    @staticmethod
    def create_schedule(additional_data: dict) -> Schedule:
        schedule = Schedule()

        if 'BOUNDS' in additional_data.keys():
            bounds = additional_data['BOUNDS']
            schedule.bounds = pd.DataFrame(bounds)
            df = ScheduleConstructor.rename(schedule.bounds)
            schedule.bounds = DebitLimitsConstructor.create_debit_limits_sch(df)

        if 'MAKEGROUPLIST' in additional_data.keys():
            groups = additional_data['MAKEGROUPLIST']
            new_groups =dict()
            for group in groups:
                new_groups[list(group.keys())[0]] = group[list(group.keys())[0]]
            schedule.groups = new_groups

        return schedule

    @staticmethod
    def rename(df: pd.DataFrame) -> pd.DataFrame:
        names = list(df.columns)
        names_dict = dict()
        for name in names:
            names_dict[name] = name.lower()

        df.rename(names_dict)
        return df
