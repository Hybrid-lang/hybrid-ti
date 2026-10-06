# -*-encoding=utf-8-*-
# TODO: 这些代码完全不要用，需要自己理解，这只是参考！！！
class Env:
    def __init__(self, parent=None):
        self.vars = {}          # 本作用域的变量表
        self.parent = parent    # 父作用域（外层）

    def var(self, name, value):
        """声明新变量（写在本层）"""
        self.vars[name] = value

    def lookup(self, name):
        """查找变量（从内往外爬）"""
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.lookup(name)
        raise NameError(f"变量 '{name}' 未定义")

    def assign(self, name, value):
        """修改变量（找到它所在的那一层改）"""
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"变量 '{name}' 未定义")
