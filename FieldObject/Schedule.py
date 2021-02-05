import pandas as pd


class Schedule:
    def __init__(self):
        self.bounds = None
        self.groups = None


class ScheduleConstructor:

    @staticmethod
    def create_schedule(additional_data: dict) -> Schedule:
        schedule = Schedule()

        if 'BOUNDS' in additional_data.keys():
            bounds = additional_data['BOUNDS']
            schedule.bounds = pd.DataFrame(bounds)

        if 'MAKEGROUPLIST' in additional_data.keys():
            groups = additional_data['MAKEGROUPLIST']
            schedule.groups = pd.DataFrame.from_dict(groups)

        return schedule
