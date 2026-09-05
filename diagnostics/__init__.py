"""
diagnostics/
├── __init__.py
├── span.py               # 位置信息（文件、行、列、长度）
├── codes.py              # 错误码字典（E001, W002...）
├── diagnostic.py         # 错误/警告长什么样
└── reporter.py           # 核心：收集、打印
"""
from .reporter import Reporter

__all__ = ["Reporter"]
