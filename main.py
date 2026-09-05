# -*-encoding=utf-8-*-
# Hybrid Toy Interpreter
import argparse

parser = argparse.ArgumentParser(description='hybrid-ti')
parser.add_argument('path', type=str, help='file path')
args = parser.parse_args()

from frontend import clean_notation, Lexer
from diagnostics import Reporter

code = ""
f = open(args.path, "r", encoding = "utf-8")
code = f.read()
f.close()

cleaned = clean_notation(code)

reporter = Reporter(args.path, code)
lexer = Lexer(cleaned, reporter)
lexer.tokenize()

print(cleaned)
print(lexer.tokens)
reporter.emit_all()
