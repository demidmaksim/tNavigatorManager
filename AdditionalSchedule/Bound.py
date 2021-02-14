import pandas as pd


class DebitLimits:

    well = 'well'
    valve = 'valve/segment'
    date = 'date'
    min_liq = 'min liquid'
    max_liq = 'max liquid'
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
            new_df.loc[new_df.shape[0], DebitLimits.date] = date
            new_df.sort_values(DebitLimits.date)
            new_df = new_df.interpolate(method='pad')
            return new_df.iloc[len(new_df)-1]

        else:
            new_df.loc[new_df.shape[1] - 1, DebitLimits.date] = date
            new_df[DebitLimits.well] = well
            new_df[DebitLimits.valve] = segment
            new_df[DebitLimits.min_liq] = 0
            new_df[DebitLimits.max_liq] = float('inf')
            new_df[DebitLimits.fluid] = 'FLUID'
            return new_df


class DebitLimitsConstructor:

    @staticmethod
    def create_debit_limits_schedule(df) -> DebitLimits:
        debit_limits = DebitLimits()
        df = DebitLimitsConstructor.prepare_date(df)
        debit_limits.df = df
        return debit_limits

    @staticmethod
    def prepare_date(df) -> pd.DataFrame:
        dates = pd.to_datetime(df[DebitLimits.date])
        df[DebitLimits.date] = dates
        return df
