# -*-encoding=utf-8-*-
# diagnostics/diagnostic.py
import io
from dataclasses import dataclass
from .span import Span
from .codes import ErrorCode

@dataclass
class Diagnostic:
    """一条完整的诊断报告"""
    code: ErrorCode          # 使用上面定义的 E001 等
    msg: str             # 具体的错误描述
    file: str
    line: str
    col: str
    source: str

    def read_contest(self):
        now = 1
        for i in io.StringIO(self.source):  # 注意这会保留每行末尾的 \n
            if now == self.line:
                return i.rstrip("\n")
            now += 1

    def to_string(self) -> str:
        """将诊断转换为纯文本（给 Reporter 调用）"""
        if self.code.code[0] == "E":
            level = "error"
        else:
            level = "warning"
        base = f"{level}[{self.code.code}]: {self.code.description.format(*self.msg)}\n"
        base += f"--> {Span(self.file, self.line, self.col)}\n"
        base += f"{self.line} | {self.read_contest()}"
        return base