from pycparser import c_parser, c_ast, parse_file,c_generator
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment
import time

class BaseErrorModel:
    def __init__(self, ast):
        self.declList = []
        self.forList = []
        self.ifList = []
        self.funDefList = []
        self.blockItemList = []
        self.ast = ast
        self._coll_nodes()


    def _dfs(self, node):
        if isinstance(node, Node):
            if isinstance(node, For):
                self.forList.append(node)
            elif isinstance(node, Decl):
                self.declList.append(node)
            elif isinstance(node, If):
                self.ifList.append(node)
            elif isinstance(node, FuncDef):
                self.funDefList.append(node)
            elif isinstance(node, Compound):
                self.blockItemList.append(node.block_items)
            nodes = node.children()
            if nodes:
                for i in nodes:
                    self._dfs(i)
        elif isinstance(node, tuple):
            for i in node:
                self._dfs(i)

    def generate_error(self,error_list,**args):
        pass

    def generate_error_default(self):
        pass


    def show_ast(self):
        print(self.ast.children())

    def _coll_nodes(self):
        for i in self.ast.children():
            self._dfs(i[1])

    # 返回所有变量及变量类型
    def coll_variable(self):
        return self.declList

    def coll_block_items(self):
        return self.blockItemList


    def coll_if_body(self):
        return self.ifList

    # 返回所有循环体
    def coll_loop_body(self):
        return self.forList


    # 返回所有方法名及参数和参数类型
    def coll_function(self):
        return self.funDefList

