from .Components.SMSPEC.SMSPECReader import *
from .Components.UNSMRY.UNSMRYReader import *
from .SUMMARY import *


class SUMMARYReader:
    """
    Класс для чтения SUMMARY файлов.
    """
    def __init__(self, smspec_link: str):
        self.SMSPEC = SMSPECWorkerConstructor.from_file(smspec_link)
        self.UNSMRY = UNSMRYLoader(smspec_link.replace('SMSPEC', 'UNSMRY'))

    def report(self):
        self.SMSPEC.report()

    def __get_dimension(self, names: str or list):
        time_length = self.SMSPEC.time.get_number_of_step()
        if type(names) == list:
            name_length = len(names)
        else:
            name_length = 1
        return time_length, name_length

    def get(self, names: str or list, keywords: str or list,
            nums: int or list) -> SUMMARY:

        start, length = self.SMSPEC.get_read_vector(names, keywords, nums)
        dimension = self.__get_dimension(names)
        data = self.UNSMRY.get_from_file(start, length, dimension)
        position_matrix = self.SMSPEC.get_position_matrix(names, keywords, nums)

        return SUMMARY(position_matrix, data)

    def get_all_vector(self):
        well_name = self.SMSPEC.storage.target_name[0]
        keywords = self.SMSPEC.storage.get_smsmpec_data('KEYWORDS')
        names = self.SMSPEC.storage.get_smsmpec_data(well_name)
        nums = self.SMSPEC.storage.get_smsmpec_data('NUMS')
        return keywords, names, nums
