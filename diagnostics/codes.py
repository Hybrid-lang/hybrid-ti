# -*-encoding=utf-8-*-
"""
错误码格式：E(W)XXxxx
E：错误
W：警告
XX：错误大类
xxx：具体错误

E00xxx：意外的错误
E01xxx：词法错误
E02xxx：语法错误
E03xxx：
"""
from dataclasses import dataclass

@dataclass(slots = True)
class Code:
    code: str
    description: str

@dataclass(slots = True)
class ErrorCode(Code):
    pass

@dataclass(slots = True)
class WarningCode(Code):
    pass

# AST根节点中出现意外的空值。如果看到此消息，请向开发人员报告。
E00001 = ErrorCode("E00001-unexpected", "unexpected null value in the root node of AST\nif you see this message, please report it to the developers")

# 未知的字符“{}”
E01001 = ErrorCode("E01001", "unknown character \"{}\"")
# 数字中多余的小数点
E01002 = ErrorCode("E01002", "extra decimal point in the number")

# 缩进时不能同时使用空格和制表符
E02001 = ErrorCode("E02001", "spaces and tabs cannot be mixed in indentation")
# 使用了 {} 个空格进行缩进，而 {} 不是4的倍数
E02002 = ErrorCode("E02002", "{} {} {} used for indentation, while is not a multiple of 4")
# 未匹配的 “(”
E02003 = ErrorCode("E02003", "unmatched \"(\"")
# 多余的 “)”
E02004 = ErrorCode("E02004", "extra \")\"")
# 一元运算符缺少右操作数
E02005 = ErrorCode("E02005", "unary operator missing right operand")
# 二元运算符缺少左操作数
E02006 = ErrorCode("E02006", "binary operator missing left operand")
# 二元运算符缺少右操作数
E02007 = ErrorCode("E02007", "binary operator missing right operand")
# 额外的缩进
E02008 = ErrorCode("E02008", "extra indentation")
# 定义变量时缺少变量名称
E02009 = ErrorCode("E02009", "missing variable name when defining the variable")
# 无效的变量名
E02010 = ErrorCode("E02010", "invalid variable name")
