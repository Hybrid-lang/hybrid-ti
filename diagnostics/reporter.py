# diagnostics/reporter.py
import sys
from typing import List
from .diagnostic import Diagnostic
from .span import Span
from .codes import *


class Reporter:
    def __init__(self, file_, source):
        self.file = file_
        self.source = source
        self.diagnostics: List[Diagnostic] = []

    # ---------- 添加错误（供 Lexer / Parser 批量收集） ----------
    def __add(self, diag: Diagnostic):
        self.diagnostics.append(diag)

    def code_class(self, code):
        match code:
            case "E01001":
                return E01001
            case "E02001":
                return E02001
            case "E02002":
                return E02002

    # ---------- 便捷方法：快速添加上下文错误 ----------
    def error(self, code, msg, line, col):
        self.__add(Diagnostic(self.code_class(code), msg, self.file, line, col, self.source))

    def warning(self, code, msg, file, line, col):
        self.error(code, msg, file, line, col)

    # ---------- 运行时专用：发现致命错误立即退出 ----------
    def fatal(self, code, msg, line, col):
        """用于运行时（Evaluator），立刻打印并退出"""
        diag = Diagnostic(self.code_class(code), msg, self.file, line, col, self.source)
        self._emit_one(diag)
        sys.exit(1)

    # ---------- 输出逻辑 ----------
    def emit_all(self):
        """打印所有收集到的错误（用于编译阶段）"""
        errors = 0
        warnings = 0
        if not self.diagnostics:
            return
        for diag in self.diagnostics:
            if diag.code.code[0] == "E":
                errors += 1
            else:
                warnings += 1
            print(diag.to_string())
            print()

        print(f"{errors} {'errors' if errors > 1 else 'error'}, {warnings} {'warnings' if warnings > 1 else 'warning'}")

        # 如果有错误，退出（但保留错误码给调用者）
        if any(d.code.code[0] == "E" for d in self.diagnostics):
            sys.exit(1)

    def _emit_one(self, diag: Diagnostic):
        """立即打印单条错误，不经过列表"""
        print(diag.to_string())
