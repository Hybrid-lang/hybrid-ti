# -*-encoding=utf-8-*-
from .values import IntValue, FltValue


class Runner:
    def __init__(self, ast, reporter):
        self.ast = ast
        self.reporter = reporter

    def run(self):
        pass
