import pandas as pd
from Eclipse_Binary_Parser.BaseBinaryWorker.BinaryReader import *


class Storage:
    """
    Класс для хранения ифнормации о порядке записи данных в UNSMRY файлах
    """
    def __init__(self, df: pd.DataFrame, target_name: list):
        self.__df = df
        self.target_name = target_name

    def _get_df(self):
        return self.__df

    def get_number_of_word(self) -> int:
        return self.__df.shape[0]

    def get_time_position(self, keyword) -> np.array:
        keyword_pattern = self.__df['KEYWORDS'] == keyword
        return [self.__df[keyword_pattern].index[0]]

    def get_position(self, name: str or None, keyword: str,
                     num: int or None) -> int:

        keyword_pattern = self.__df['KEYWORDS'] == keyword

        if name is not None:
            name_pattern = self.__df[self.target_name[0]] == name
        else:
            name_pattern = ~self.__df[self.target_name[0]].isnull()

        if num is None:
            num_pattern = ~self.__df['NUMS'].isnull()
        else:
            num_pattern = self.__df['NUMS'] == num

        pattern = name_pattern & keyword_pattern & num_pattern

        return self.__df[pattern].index[0]

    def get_list_position(self, names: list, kwords: list, nums: list) -> list:
        positions = list()

        for name_id, name in enumerate(names):
            keyword = kwords[name_id]
            num = nums[name_id]
            ind = self.get_position(name, keyword, num)
            positions.append(ind)

        return positions

    def get_smsmpec_data(self, keyword):
        return self.__df[keyword]

    def report(self):
        sk = list(self.__df.keys())
        fo = list(pd.unique(self.__df[self.target_name[0]]))
        mk = list(pd.unique(self.__df[self.target_name[1]]))
        print('SMSPEC Keyword:\t{}'.format(sk))
        print('Field Object:\t{}'.format(fo))
        print('Model Keyword (Mnemonic):\t{}'.format(mk))


class StorageConstructor:

    @staticmethod
    def __get_target_name(keys: list) -> list or None:
        if 'WGNAMES' in keys and 'NAMES' not in keys:
            return ['WGNAMES', 'KEYWORDS', 'NUMS', 'UNITS']
        elif 'NAMES' in keys and 'WGNAMES' not in keys:
            return ['NAMES', 'KEYWORDS', 'NUMS', 'UNITS']
        else:
            return None

    @staticmethod
    def from_file(link: str) -> Storage:
        binary_file = BinaryReader(link)
        binary_file.reading_all_file()

        all_key = list(binary_file.data.keys())
        target_key = StorageConstructor.__get_target_name(all_key)

        dict_for_df = dict()
        for key in target_key:
            dict_for_df[key] = binary_file.data[key].value
        df = pd.DataFrame.from_dict(dict_for_df)

        tar_n = target_key
        return Storage(df, tar_n)
