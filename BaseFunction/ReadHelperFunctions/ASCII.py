KeyWords = ['INFLOWZO']


def this_is_skip(line) -> bool:
    if line == '' or line[:2] == '--':
        return True
    else:
        return False


def this_is_keyword(line: str) -> bool:
    if line.split()[0] in KeyWords:
        return True
    else:
        return False


def clean_from_comment(line: str) -> str:
    line = line.strip().upper()
    line = line.split('--')[0]
    line = line.split('#')[0]
    line = line.split('%')[0]
    return line.strip()


def this_is_end_keyword(line: str) -> bool:
    if line.split()[0] == '/':
        return True
    else:
        return False
