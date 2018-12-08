from error_models.base_error_model import BaseErrorModel
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment
import random
class OutOfIndexErrorModel(BaseErrorModel):

    def __init__(self,ast):
        super().__init__(ast)
        self.loop_node_list = []
        self._coll_loop_node()

    def _coll_loop_node(self):
        for node in self.node_list:
            if isinstance(node, For):
                self.loop_node_list.append(node)


    def generate_error(self, loop_body_list):
        for node in loop_body_list:
            if hasattr(node.cond.right,'value'):
                value = int(node.cond.right.value) + 1
                node.cond.right.value = value
        return self.ast

    def generate_error_random(self):
        random_loop_node_list = []
        for i in self.loop_node_list:
            n = random.randint(0, 1)
            if n == 0:
                random_loop_node_list.append(i)
        ast = self.generate_error(random_loop_node_list)
        return ast

    def generate_error_default(self):
        ast = self.generate_error(self.loop_node_list)
        return ast