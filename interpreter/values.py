# -*-encoding=utf-8-*-
from dataclasses import dataclass

@dataclass(slots = True)
class IntValue:
    value: str

@dataclass(slots = True)
class FltValue:
    value: str
