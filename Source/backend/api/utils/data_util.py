# from string_utils import *


def isBlank(str: any) -> bool:
    return not isNotBlank(str)


def isNotBlank(str: any) -> bool:
    if str is None:
        return False
    if type(str) is str:
        return bool(str and str.strip())
    else:
        return bool(str)
