import pandas as pd


class initialization:
    def __init__(self):
        self.crutch = Crutch()
        self.SMMC = StrategyManagerModelConstructor()

    def create_results_folder(self):
        link_folder = self.crutch.get_report_folder()
        print(link_folder)
        os.makedirs(link_folder)

    def save_df(self, df: pd.DataFrame):
        self.create_results_folder()
        link = self.crutch.get_csv_results_file()
        df.to_csv(link)

    def create_dataframe(self,
                         str_man_mod: StrategyManagerModel) -> pd.DataFrame:
        df = pd.DataFrame()
        df['time'] = [np.nan]
        for inflowzone in str_man_mod.get_all_inflow_zones():
            for param in self.crutch.params:
                name = "{0}_{1}_{2}".format(inflowzone.well,
                                            inflowzone.segment,
                                            param)
                df[name] = [0]

        for well in str_man_mod.get_all_well():
            for param in self.crutch.params:
                name = "{0}_1_{1}".format(well.name, param)
                df[name] = [0]
        return df

    @staticmethod
    def record_first_step(str_man_mod: StrategyManagerModel,
                          df: pd.DataFrame) -> pd.DataFrame:
        for inflowzone in str_man_mod.get_all_inflow_zones():
            name = "{0}_{1}_SVAL".format(inflowzone.well, inflowzone.segment)
            df[name][len(df) - 1] = inflowzone.fully_open_size
        return df

    def start_with_pandas(self):
        self.crutch.create_log()
        str_man_mod = self.SMMC.construct_for_init()
        mdf = self.create_dataframe(str_man_mod)
        mdf = self.record_first_step(str_man_mod, mdf)
        self.save_df(mdf)


def __init_script__():
    print('0')
    init = initialization()
    print('1')
    init.start_with_pandas()
    print("Успешно инициализировано!")


def field_management_manager():
    print('0')
    str_man_mod_const = StrategyManagerModelConstructor()
    print('1')
    str_man_mod = str_man_mod_const.construct()
    print('2')
    str_man_mod.save_with_pandas(str_man_mod.Crutch.get_csv_results_file())
    print("Успешно!")

