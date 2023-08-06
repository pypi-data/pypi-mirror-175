import os as _os
from typing import Callable


def system(__command: str):
    return _os.system(command=__command)


def join_paths(__name, branch):
    return _os.path.join(__name, branch)


def abspath(__name: str, is_abspath: bool = False):
    return __name if is_abspath else _os.path.abspath(__name)


def basename(__name: str):
    return __name.split("/")[-1] if "/" in __name else __name


def scandir(__name: str, is_abspath: bool, where: Callable[[object], bool] = None):
    result = _os.scandir(__name, is_abspath=is_abspath)
    if where is not None:
        result = (file for file in result if where(file))
    return result


def parentdir(__name: str, is_abspath: bool = False):
    result = abspath(__name, is_abspath=is_abspath)
    if "/" in result:
        components = result.split("/")[:-1]
        result = "/".join(components)
    return result
