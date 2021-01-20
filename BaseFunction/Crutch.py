import os
import pandas as pd
import datetime as dt


def get_project_folder():
    return os.getcwd()


def get_additional_schedule_link() -> str:
    folder = get_project_folder().replace('/', '\\') + '\\'
    return folder + Crutch.additional_schedule_name


class Crutch:
    KeyWords = ['INFLOWZO']
    python_log = 'python_algorithm.log'
    params = ['SLPR', 'SWFR', 'SOFR', 'SPR', 'SPRD', 'SVAL']
    additional_schedule_name = 'Additional Schedule.INC'

    @staticmethod
    def get_error_pattern(df: pd.DataFrame, name_sofr: str = 'SOFR',
                          name_swfr: str = 'SWFR') -> pd.DataFrame:
        return df[name_sofr] * df[name_swfr] < 0

    @staticmethod
    def get_current_time() -> str:
        now = dt.datetime.now()
        return now.strftime("%Y_%m_%d__%H.%M.%S")

    @staticmethod
    def supplement_log(keyword: str, data: str) -> None:
        # Дописать
        data = data.replace('\n', '\t//\t')
        with open(Crutch.python_log, 'a+') as file:
            file.write(keyword + ': ' + data)

    @staticmethod
    def get_start_time() -> str or None:
        with open(Crutch.python_log, 'r') as file:
            for line in file:
                if 'start_time:' in line:
                    start_time = line.split('start_time:')[1].strip()
                    break
        return start_time

    def create_log(self) -> None:
        # Дописать
        with open(Crutch.python_log, 'w') as file:
            start_time = self.get_current_time()
            file.write('start_time: ' + start_time)

    def get_report_folder(self) -> str:
        folder = get_project_folder()
        start_time = self.get_start_time()
        return folder + '\\' + 'Python_Algorithm_Results' + '\\' + start_time

    def get_xlsx_results_file(self) -> str:
        return self.get_report_folder() + '\\' + self.get_start_time() + '.xlsx'

    def get_csv_results_file(self) -> str:
        return self.get_report_folder() + '\\' + self.get_start_time() + '.CSV'
