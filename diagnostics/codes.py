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

E00001 = ErrorCode("E00001-unexpected", "unexpected null value in the root node of AST\nif you see this message, please report it to the developers")

E01001 = ErrorCode("E01001", "unknown character \"{}\"")

E02001 = ErrorCode("E02001", "spaces and tabs cannot be mixed in indentation")
E02002 = ErrorCode("E02002", "{} {} {} used for indentation, while is not a multiple of 4")
E02003 = ErrorCode("E02003", "unmatched \"(\"")
E02004 = ErrorCode("E02004", "extra \")\"")
E02005 = ErrorCode("E02005", "unary operator missing right operand")
E02006 = ErrorCode("E02006", "binary operator missing left operand")
E02007 = ErrorCode("E02007", "binary operator missing right operand")
