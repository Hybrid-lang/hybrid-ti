# -*-encoding=utf-8-*-
from dataclasses import dataclass
from copy import deepcopy
from .kinds import TokenType


@dataclass(slots=True)
class AstNode:
    line: int
    col: int


@dataclass(slots=True)
class Root(AstNode):
    body: list[AstNode]


@dataclass(slots=True)
class IntLit(AstNode):
    value: str


@dataclass(slots=True)
class FltLit(AstNode):
    value: str


@dataclass(slots=True)
class UnaryExpr(AstNode):
    op: str
    right: AstNode


@dataclass(slots=True)
class BinExpr(AstNode):
    op: str
    left: AstNode
    right: AstNode


class Parser:
    def __init__(self, tokens, reporter):
        self.pos = 0
        self.tokens = tokens
        self.__len = len(tokens)
        self.prec = {
            TokenType.PIPE_PIPE: 1,
            TokenType.AMP_AMP: 2,
            TokenType.TILDE_TILDE: 3,
            TokenType.EQ_EQ: 10,
            TokenType.BANG_EQ: 10,
            TokenType.GT: 10,
            TokenType.LT: 10,
            TokenType.GT_EQ: 10,
            TokenType.LT_EQ: 10,
            TokenType.PLUS: 20,
            TokenType.MINUS: 20,
            TokenType.STAR: 30,
            TokenType.SLASH: 30,
            TokenType.SLASH_SLASH: 30,
            TokenType.PERCENT: 30,
            TokenType.STAR_STAR: 50
        }
        self.line = tokens[0].line
        self.col = tokens[0].col
        self.ast = Root(1, 1, [])
        self.reporter = reporter

        # tmp = []
        # for i in token:
        #    if i.tpye == TokenType.NEWLINE:
        #        self.tokens.append(deepcopy(tmp))
        #        tmp = []
        #    else:
        #        tmp.append(i)

    def peek(self):
        return self.tokens[self.pos] if self.pos < self.__len else None

    def consume(self):
        token = self.peek()

        if token is None:
            return None

        self.pos += 1

        self.line = token.line
        self.col = token.col

        return token

    def parse_expr_line(self, min_prec=0):
        if self.peek() is None:
            return

        if self.peek().type in (TokenType.PLUS, TokenType.MINUS, TokenType.TILDE_TILDE):
            match self.peek().type:
                case TokenType.PLUS:
                    op = "+"
                case TokenType.MINUS:
                    op = "-"
                case TokenType.TILDE_TILDE:
                    op = "~~"
            self.consume()
            start_line, start_col = self.line, self.col
            right = self.parse_expr_line(40)
            left = UnaryExpr(start_line, start_col, op, right)
        else:
            left = self.parse_primary()

        while True:
            token = self.peek()

            if token is None or token.type not in self.prec:
                break

            if self.prec[token.type] < min_prec:
                break

            self.consume()
            start_line, start_col = self.line, self.col
            prec = self.prec[token.type]
            next_prec = prec + 1 if token.type != TokenType.STAR_STAR else prec
            right = self.parse_expr_line(next_prec)

            match token.type:
                case TokenType.PLUS:
                    op = "+"
                case TokenType.MINUS:
                    op = "-"
                case TokenType.STAR:
                    op = "*"
                case TokenType.STAR_STAR:
                    op = "**"
                case TokenType.SLASH:
                    op = "/"
                case TokenType.SLASH_SLASH:
                    op = "//"
                case TokenType.PERCENT:
                    op = "%"
                case TokenType.EQ_EQ:
                    op = "=="
                case TokenType.BANG_EQ:
                    op = "!="
                case TokenType.GT_EQ:
                    op = ">="
                case TokenType.LT_EQ:
                    op = "<="
                case TokenType.GT:
                    op = ">"
                case TokenType.LT:
                    op = "<"
                case TokenType.AMP_AMP:
                    op = "&&"
                case TokenType.PIPE_PIPE:
                    op = "||"
            left = BinExpr(start_line, start_col, op, left, right)

        return left

    def parse_primary(self):
        token = self.peek()

        if token.type == TokenType.NUM:
            self.consume()
            return IntLit(self.line, self.col, token.value)
        elif token.type == TokenType.LPAREN:
            self.consume()
            node = self.parse_expr_line(0)
            self.consume()
            return node

    def parse_expr(self):
        while True:
            node = self.parse_expr_line()
            if self.peek() is None:
                break
            elif self.peek().type == TokenType.NEWLINE:
                self.consume()

            if node is not None:
                self.ast.body.append(node)
