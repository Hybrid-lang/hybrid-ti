# -*-encoding=utf-8-*-
"""
interpreter/           # 解释器核心
├── __init__.py
├── values.py        # 运行时值系统（IntValue, FloatValue, StringValue...）
├── environment.py   # 作用域链（变量存储与查找）
├── evaluator.py     # AST 求值器（核心，match-case 遍历 AST）
└── builtins.py      # 内置函数（print, len, range...）
"""
from .evaluator import Runner

__all__ = ["Runner"]