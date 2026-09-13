# -*-encoding=utf-8-*-
from enum import IntEnum, auto

class TokenType(IntEnum):
    NULL = 0
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    NUM = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    STAR_STAR = auto()
    SLASH = auto()
    SLASH_SLASH = auto()
    PERCENT = auto()
    EQ_EQ = auto()
    GT_EQ = auto()
    LT_EQ = auto()
    BANG_EQ = auto()
    GT = auto()
    LT = auto()
    AMP_AMP = auto()
    PIPE_PIPE = auto()
    TILDE_TILDE = auto()
    LPAREN = auto()
    RPAREN = auto()
