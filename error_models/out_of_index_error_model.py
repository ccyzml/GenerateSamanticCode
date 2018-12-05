from error_models.base_error_model import BaseErrorModel
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment

class OutOfIndexErrorModel(BaseErrorModel):
    def generate_error(self, loop_body_list):
        for node in loop_body_list:
            if hasattr(node.cond.right,'value'):
                value = int(node.cond.right.value) + 1
                node.cond.right.value = value
        return self.ast

    def generate_error_default(self):
        ast = self.generate_error(self.coll_loop_body())
        return ast