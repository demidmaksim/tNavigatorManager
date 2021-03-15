"""
Раздел вспомогательных функций для чтения ASCII файлов
"""


def this_is_skip(line) -> bool:
    """
    Проверяет необходимость пропустить эту строку
    """
    if line == '' or line[:2] == '--':
        return True
    else:
        return False


def clean_from_comment(line: str) -> str:
    """
    Отчищает от комментариев
    """
    line = line.strip().upper()
    line = line.split('--')[0]
    line = line.split('#')[0]
    line = line.split('%')[0]
    return line.strip()


def this_is_end_keyword(line: str) -> bool:
    """
    Проверка строки на конец ключевого слова
    """
    if line == '':
        return False
    else:
        pass

    if line.split()[0].lower() == 'end':
        return True
    else:
        return False
