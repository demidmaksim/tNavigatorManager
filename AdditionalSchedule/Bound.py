import pandas as pd


class DebitLimits:
    def __init__(self):
        self.df = None

    def get_limit(self, date, well, segment):

        pattern1 = self.df['well'] == well

        if segment is not None:
            pattern2 = self.df['valve/segment'] == segment
        else:
            pattern2 = self.df['valve/segment'].isna()

        pattern3 = self.df['date'] <= date
        pattern = pattern1 & pattern2 & pattern3

        new_df = self.df[pattern]

        if new_df.shape[0] != 0:
            new_df.loc[new_df.shape[0], 'date'] = date
            new_df.sort_values('date')
            new_df = new_df.interpolate(method='pad')
            pattern = new_df['date'] == date
            pattern = pd.DataFrame(pattern)

            if pattern.shape[0] > 1:
                return new_df[pattern]
            else:
                return new_df[pattern][0]

        else:
            new_df.loc[new_df.shape[1] - 1, 'date'] = date
            new_df['well'] = well
            new_df['valve/segment'] = segment
            new_df['min liquid'] = 0
            new_df['max liquid'] = float('inf')
            new_df['fluid'] = 'FLUID'
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
        dates = pd.to_datetime(df['date'])
        df['date'] = dates
        return df
