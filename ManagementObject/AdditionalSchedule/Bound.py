import pandas as pd
import datetime as dt


class DebitLimits:

    well = 'well'
    valve = 'valve/segment'
    date = 'date'
    min_vol = 'min liquid'
    max_vol = 'max liquid'
    fluid = 'fluid'

    def __init__(self):
        self.df = None

    def __get_target_value(self, date, well, segment, special_fluid):

        pattern1 = self.df[DebitLimits.well].values == well

        if segment is not None:
            pattern2 = self.df[DebitLimits.valve].values == segment
        else:
            pattern2 = self.df[DebitLimits.valve].isna()

        pattern3 = self.df[DebitLimits.date] <= date
        if special_fluid is None:
            pattern = pattern1 & pattern2 & pattern3
        else:
            pattern4 = self.df[DebitLimits.fluid] == special_fluid
            pattern = pattern1 & pattern2 & pattern3 & pattern4

        return self.df[pattern]

    def get_limit(self, date: dt, well: str, segment: int,
                  special_fluid: str) -> dict:
        """
        Возвращает лимит по текущей скважине из дополнительного расписания.
        :param date: текущая дата
        :param well: имя скважины
        :param segment: имя сегмента приуроченого к данной скважине
        :param special_fluid: имя флюида (нефть/жидкость)
         по которому ищится ограничение
        """
        new_df = self.__get_target_value(date, well, segment, special_fluid)

        if new_df.shape[0] != 0:
            results = {
                DebitLimits.date: date,
                DebitLimits.well: new_df[DebitLimits.well].values[-1],
                DebitLimits.valve: new_df[DebitLimits.valve].values[-1],
                DebitLimits.min_vol: new_df[DebitLimits.min_vol].values[-1],
                DebitLimits.max_vol: new_df[DebitLimits.max_vol].values[-1],
                DebitLimits.fluid: new_df[DebitLimits.fluid].values[-1]
            }
            return results

        else:
            results = {
                DebitLimits.date: date,
                DebitLimits.well: well,
                DebitLimits.valve: segment,
                DebitLimits.min_vol: 0,
                DebitLimits.max_vol: float('inf'),
                DebitLimits.fluid: 'LIQUID'
            }

            return results


class DebitLimitsConstructor:

    @staticmethod
    def create_debit_limits(df: pd.DataFrame) -> DebitLimits:
        """
        Создает экземпляр класса с огрничениями по дебиту нефти и жидкости
        :param df: DataFrame с огрничениями
        :return: экземляр класса DebitLimits
        """
        debit_limits = DebitLimits()
        df = DebitLimitsConstructor.prepare_date(df)
        debit_limits.df = df
        return debit_limits

    @staticmethod
    def prepare_date(df: pd.DataFrame) -> pd.DataFrame:
        """
        Кофектор столбца со временем в формат DataFrame
        :param df: исодный DataFrame
        :return: конвертированный DataFrame
        """
        dates = pd.to_datetime(df[DebitLimits.date])
        df[DebitLimits.date] = dates
        return df
