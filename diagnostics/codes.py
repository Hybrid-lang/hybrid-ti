# -*-encoding=utf-8-*-
from dataclasses import dataclass

@dataclass(slots = True)
class Code:
    code: str
    description: str

@dataclass(slots = True)
class ErrorCode(Code):
    pass

@dataclass(slots = True)
class WarningCode(Code):
    pass

E01001 = ErrorCode("E01001", "unknown character \"{}\"")

E02001 = ErrorCode("E02001", "spaces and tabs cannot be mixed in indentation")
E02002 = ErrorCode("E02002", "{} {} {} used for indentation, while is not a multiple of 4")
