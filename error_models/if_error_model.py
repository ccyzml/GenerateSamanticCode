from error_models.base_error_model import BaseErrorModel
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment
from op_swap import get_error_op
import random
class IfErrorModel(BaseErrorModel):

    def __init__(self,ast):
        super().__init__(ast)
        self.if_node_list = []
        self._coll_if_node()

    def generate_error(self, if_body_list):
       for i in if_body_list:
           n = random.randint(0,1)
           if n == 0:
             i.cond.op = get_error_op(i.cond.op)
           else:
              self._swap(i)
       return self.ast

    def generate_error_default(self):
        ast = self.generate_error(self.if_node_list)
        return ast


    def generate_error_random(self):
        random_if_node_list = []
        for i in self.if_node_list:
            n = random.randint(0,1)
            if n == 0:
                random_if_node_list.append(i)
        ast = self.generate_error(random_if_node_list)
        return ast

    def _coll_if_node(self):
        for node in self.node_list:
            if isinstance(node, If):
                self.if_node_list.append(node)

    def _swap(self,if_body):
        cond = if_body.cond
        left = cond.left
        right = cond.right
        cond.left,cond.right = right,left