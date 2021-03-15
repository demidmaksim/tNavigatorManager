from tNav.spesial import *


class MnemonicResults:
    """
    Класс для хранения данных прочитанной конкретной мнемоники
    """
    def __init__(self, well_names, num_names, values, additional):
        self.well = well_names
        self.num = num_names
        self.values = values
        self.for_ind = additional

    def get_param(self, well: str, segm: int or None) -> float:
        """
        Возвращает данные по узлу учета
        :param well: имя скважины
        :param segm: имя зона притока(секгамента)
        :return:
        """
        ind = self.for_ind.index([well, segm])
        return self.values[ind]


class AllMnemonicResults:
    """
    Класс для хранения прочитанных всех мнемоник
    """
    def __init__(self):
        self.param = dict()

    def set_param(self, keyword: str, value: MnemonicResults) -> None:
        self.param[keyword] = value

    def get_param(self, keyword: str, well: str, segm: int or None) -> list:
        return self.param[keyword].get_param(well, segm)


def read_segment_mnemonic(text: str) -> MnemonicResults:
    """
    Ключевое слово для чтения мнемоник сегментов
    :param text: Текст для интерпритации
    :return: экземпляр класса MnemonicResults
    """
    text = str(text)
    text_list = text.split('\n')

    well_names = []
    num_names = []
    values = []
    additional = []

    for line in text_list:

        if 'WELL' in line.upper():
            well_name = line.upper().split(':')[1]
            well_name = well_name.split(',')[0].strip().replace("'", '')
            well_names.append(well_name)
            num_name = line.upper().split(':')[-2]
            num_name = int(num_name.strip().replace("'", ''))
            num_names.append(num_name)
            additional.append([well_name, num_name])

        elif line.upper() != '':
            values.append(float(line.strip()))

    results = MnemonicResults(well_names, num_names, values, additional)
    return results


def read_well_mnemonic(text: str) -> MnemonicResults:

    """
    Ключевое слово для чтения мнемоник скважин
    :param text: Текст для интерпритации
    :return: экземпляр класса MnemonicResults
    """

    text = str(text)
    text_list = text.split('\n')
    well_names = []
    num_names = []
    values = []
    additional = []

    for line in text_list:
        line = line.strip()
        if ':' in line.upper():
            well_name = line.upper().strip().split(':')[0]
            well_names.append(well_name)
            num_names.append(None)
            additional.append([well_name, None])

        elif line.upper() != '':
            values.append(float(line.strip()))

    results = MnemonicResults(well_names, num_names, values, additional)
    return results


def read_target_mnemonic(target_mnemonics: list) -> AllMnemonicResults:
    """
    Читает заданные мнемоник
    :param target_mnemonics: список с необходмыми к прочтению мнемониками
    :return: экзкмпляр класса AllMnemonicResults со всеми записанными данными
    """
    all_results = AllMnemonicResults()

    for mnemonic in target_mnemonics:

        if mnemonic[0].upper() == 'W':
            results = read_well_mnemonic(eval(mnemonic))
        else:
            results = read_segment_mnemonic(eval(mnemonic))

        all_results.set_param(mnemonic, results)

    return all_results
