# -*-encoding=utf-8-*-
# Hybrid Toy Interpreter
import argparse, sys

parser = argparse.ArgumentParser(description='hybrid-ti')
parser.add_argument('path', type=str, help='file path')
args = parser.parse_args()

from frontend import clean_notation, Lexer, Parser
from diagnostics import Reporter
from interpreter import Runner

code = ""
f = open(args.path, "r", encoding = "utf-8")
code = f.read()
f.close()

if code == "":
    sys.exit(0)

cleaned = clean_notation(code)

reporter = Reporter(args.path, code)
lexer = Lexer(cleaned, reporter)
lexer.tokenize()

# 清理后源码
print(cleaned)

# 拆分后token
tokens = lexer.tokens
print(tokens)
reporter.emit_all()

parser = Parser(tokens, reporter)
parser.build_ast()

from pprint import *
# 输出AST
ast = parser.ast
pprint(ast)
# pprint(reporter.diagnostics)
reporter.emit_all()

#runner = Runner(ast, reporter)
#reporter.emit_all()
