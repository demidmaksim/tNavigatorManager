import pandas as pd


class DebitLimits:

    well = 'well'
    valve = 'valve/segment'
    date = 'date'
    min_vol = 'min liquid'
    max_vol = 'max liquid'
    fluid = 'fluid'

    def __init__(self):
        self.df = None

    def get_limit(self, date, well, segment):

        pattern1 = self.df[DebitLimits.well] == well

        if segment is not None:
            pattern2 = self.df[DebitLimits.valve] == segment
        else:
            pattern2 = self.df[DebitLimits.valve].isna()

        pattern3 = self.df[DebitLimits.date] <= date
        pattern = pattern1 & pattern2 & pattern3

        new_df = self.df[pattern]

        if new_df.shape[0] != 0:

            for_series = {
                DebitLimits.date: date,
                DebitLimits.well: new_df[DebitLimits.well].values[-1],
                DebitLimits.valve: new_df[DebitLimits.valve].values[-1],
                DebitLimits.min_vol: new_df[DebitLimits.min_vol].values[-1],
                DebitLimits.max_vol: new_df[DebitLimits.max_vol].values[-1],
                DebitLimits.fluid: new_df[DebitLimits.fluid].values[-1]
            }
            new_df = pd.Series(for_series)
            return new_df
        else:
            for_series = {
                DebitLimits.date: date,
                DebitLimits.well: well,
                DebitLimits.valve: segment,
                DebitLimits.min_vol: 0,
                DebitLimits.max_vol: float('inf'),
                DebitLimits.fluid: 'LIQUID'
            }
            new_df = pd.Series(for_series)
            return new_df


class DebitLimitsConstructor:

    @staticmethod
    def create_debit_limits_sch(df) -> DebitLimits:
        debit_limits = DebitLimits()
        df = DebitLimitsConstructor.prepare_date(df)
        debit_limits.df = df
        return debit_limits

    @staticmethod
    def prepare_date(df) -> pd.DataFrame:
        dates = pd.to_datetime(df[DebitLimits.date])
        df[DebitLimits.date] = dates
        return df
