from pycparser import c_parser, c_ast, parse_file,c_generator
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment
import time

class BaseErrorModel:
    def __init__(self, ast):
        self.node_list = []
        self.ast = ast
        self._coll_nodes()


    def _dfs(self, node):
        if isinstance(node, Node):
            self.node_list.append(node)
            nodes = node.children()
            if nodes:
                for i in nodes:
                    self._dfs(i)
        elif isinstance(node, list):
            for i in node:
                self._dfs(i)
        elif isinstance(node,tuple):
            for i in node:
                self._dfs(i)

    def generate_error(self,error_list,**args):
        pass

    def generate_error_default(self):
        pass

    def generate_error_random(self):
        pass

    def show_ast(self):
        print(self.ast.children())

    def _coll_nodes(self):
        for i in self.ast.children():
            self._dfs(i[1])


