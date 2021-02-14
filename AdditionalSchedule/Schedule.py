import pandas as pd
from AdditionalSchedule.Bound import *


class Schedule:
    def __init__(self):
        self.bounds = None
        self.groups = None

    def get_current_boundaries(self, now_time):

        dict_fo_df = dict()
        for key in self.bounds.columns:
            if key == 'date':
                dict_fo_df[key] = now_time
            else:
                dict_fo_df[key] = None

        add_df = pd.DataFrame(dict_fo_df, index=[0])
        self.bounds.append(add_df, ignore_index=True)

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
            schedule.bounds = DebitLimitsConstructor.create_debit_limits_schedule(df)

        if 'MAKEGROUPLIST' in additional_data.keys():
            groups = additional_data['MAKEGROUPLIST']
            schedule.groups = pd.DataFrame.from_dict(groups)

        return schedule

    @staticmethod
    def rename(df: pd.DataFrame) -> pd.DataFrame:
        names = list(df.columns)
        names_dict = dict()
        for name in names:
            names_dict[name] = name.lower()

        df.rename(names_dict)
        return df
