# -*-encoding=utf-8-*-
from dataclasses import dataclass


@dataclass
class Span:
    """代码片段的位置跨度（不可变）"""
    file: str  # 文件名或 "<input>"
    line: int  # 起始行（从1开始）
    col: int  # 起始列（从1开始）

    def __repr__(self):
        return f"{self.file}:{self.line}:{self.col}"
