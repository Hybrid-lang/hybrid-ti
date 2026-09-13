# -*-encoding=utf-8-*-
from .kinds import TokenType

# 容器用带 __slots__ 的类（兼顾可读性与内存）
class Token:
    __slots__ = ('type', 'value', 'line', 'col')

    def __init__(self, type_, line, col, value=None):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.col})"
        else:
            return f"Token({self.type.name}, {self.line}:{self.col})"


class Lexer:
    def __init__(self, code, reporter):
        self.code = code
        self.__len = len(code)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []

        self.indent_stack = [0]
        self.paren_depth = 0

        self.reporter = reporter

    def peek(self):
        return self.code[self.pos] if self.pos < self.__len else None

    def consume(self):
        ch = self.peek()

        if ch is None:
            return None

        self.pos += 1

        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1

        return ch

    def consume_indent(self, line, col):
        """
        统计行首的缩进，并换算成抽象的缩进级别（整数）。
        返回的级别用于和 indent_stack 栈顶比较。
        """
        spaces = 0
        tabs = 0

        # 1. 统计连续的空格和 Tab
        while True:
            ch = self.peek()
            if ch == ' ':
                spaces += 1
                self.consume()
            elif ch == '\t':
                tabs += 1
                self.consume()
            else:
                break

        # 2. 检查致命错误：混用空格和 Tab（工业级语言必须禁止）
        if spaces > 0 and tabs > 0:
            self.reporter.error(
                "E02001",
                (),
                line,
                col
            )
            # raise TabError("缩进中混用了 Tab 和空格，这是不允许的")

        # 3. 换算为级别
        if tabs > 0:
            # 每个 Tab 代表一级缩进
            return tabs
        else:
            # 空格必须严格为 4 的倍数
            if spaces % 4 != 0:
                self.reporter.error(
                    "E02002",
                    (
                        spaces,
                        "spaces" if spaces > 1 else "space",
                        "were" if spaces > 1 else "was"
                    ),
                    line,
                    col
                )
                # raise IndentationError(f"缩进使用了 {spaces} 个空格，不是 4 的倍数")
            return spaces // 4

    def emit(self, type_, line, col, value=None):
        token = Token(type_, line, col, value)
        self.tokens.append(token)

    def tokenize(self):
        while self.peek() is not None:
            start_line, start_col = self.line, self.col
            ch = self.peek()

            if ch == "\n" or ch == " " or ch == "\t":
                if ch == "\n":
                    self.consume()
                    self.emit(TokenType.NEWLINE, start_line, start_col)

                    start_line += 1
                    start_col = 1

                if self.pos == 0 or ch == "\n":
                    if self.paren_depth == 0:
                        level = self.consume_indent(start_line, start_col)
                        now = self.indent_stack[-1]
                        if level > now:
                            for i in range(level - now):
                                self.emit(TokenType.INDENT, start_line, start_col)
                            self.indent_stack.append(level)
                        elif level < now:
                            for i in range(now - level):
                                self.emit(TokenType.DEDENT, start_line, start_col)
                            self.indent_stack.pop()
                        else:
                            pass
                    else:
                        continue
                else:
                    self.consume()

            elif ch == '(':
                self.consume()
                self.paren_depth += 1
                self.emit(TokenType.LPAREN, start_line, start_col)

            elif ch == ')':
                self.consume()
                self.paren_depth -= 1
                if self.paren_depth < 0:
                    self.paren_depth = 0
                self.emit(TokenType.RPAREN, start_line, start_col)

            elif ch.isdigit():
                self.consume()
                n = ch
                if_dot = False

                while True:
                    ch = self.peek()
                    if ch is not None and ch.isdigit():
                        self.consume()
                        n += ch
                    elif ch == "." and not if_dot:
                        self.consume()
                        n += ch
                    else:
                        break

                self.emit(TokenType.NUM, start_line, start_col, n)

            elif ch == "+":
                self.consume()
                self.emit(TokenType.PLUS, start_line, start_col)

            elif ch == "-":
                self.consume()
                self.emit(TokenType.MINUS, start_line, start_col)

            elif ch == "*":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "**":
                    self.consume()
                    self.emit(TokenType.STAR_STAR, start_line, start_col)
                else:
                    self.emit(TokenType.STAR, start_line, start_col)

            elif ch == "/":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "//":
                    self.consume()
                    self.emit(TokenType.SLASH_SLASH, start_line, start_col)
                else:
                    self.emit(TokenType.SLASH, start_line, start_col)

            elif ch == "%":
                self.consume()
                self.emit(TokenType.PERCENT, start_line, start_col)

            elif ch == "=":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "==":
                    self.consume()
                    self.emit(TokenType.EQ_EQ, start_line, start_col)
                else:
                    self.reporter.error(
                        "E01001",
                        (ch),
                        start_line,
                        start_col
                    )

            elif ch == ">":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == ">=":
                    self.consume()
                    self.emit(TokenType.GT_EQ, start_line, start_col)
                else:
                    self.emit(TokenType.GT, start_line, start_col)

            elif ch == "<":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "<=":
                    self.consume()
                    self.emit(TokenType.LT_EQ, start_line, start_col)
                else:
                    self.emit(TokenType.LT, start_line, start_col)

            elif ch == "!":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "!=":
                    self.consume()
                    self.emit(TokenType.BANG_EQ, start_line, start_col)
                else:
                    self.reporter.error(
                        "E01001",
                        (ch),
                        start_line,
                        start_col
                    )
            elif ch == "&":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "&&":
                    self.consume()
                    self.emit(TokenType.AMP_AMP, start_line, start_col)
                else:
                    self.reporter.error(
                        "E01001",
                        (ch),
                        start_line,
                        start_col
                    )

            elif ch == "|":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "||":
                    self.consume()
                    self.emit(TokenType.PIPE_PIPE, start_line, start_col)
                else:
                    self.reporter.error(
                        "E01001",
                        (ch),
                        start_line,
                        start_col
                    )

            elif ch == "~":
                self.consume()
                if self.code[self.pos - 1: self.pos + 1] == "~~":
                    self.consume()
                    self.emit(TokenType.TILDE_TILDE, start_line, start_col)
                else:
                    self.reporter.error(
                        "E01001",
                        (ch),
                        start_line,
                        start_col
                    )

            else:
                self.consume()
                self.reporter.error(
                    "E01001",
                    (ch),
                    start_line,
                    start_col
                )

        for i in range(self.indent_stack[-1]):
            self.emit(TokenType.DEDENT, self.line + 1, 1)


if __name__ == "__main__":
    from diagnostics import Reporter

    code = """1+1
    2-3"""

    r = Reporter("./test.hybr", code)
    a = Lexer(code, r)
    a.tokenize()
    r.emit_all()

    print(a.tokens)
    print(a.indent_stack)
