from error_models.base_error_model import BaseErrorModel
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment,BinaryOp,Constant
from op_swap import get_error_op
import random
from pycparser import CParser
from pycparser.c_generator import CGenerator

class Missing1ErrorModel(BaseErrorModel):

    def __init__(self,ast):
        super().__init__(ast)
        self.parser = CParser()
        self.loop_node_list = []
        self._coll_loop_node()

    def _coll_loop_node(self):
        for node in self.node_list:
            if isinstance(node, For):
                self.loop_node_list.append(node)

    def generate_error(self, loop_body_list):
        for node in loop_body_list:
            cond_right = node.cond.right
            if isinstance(cond_right,BinaryOp):
                result = self._dfs_find_constant_1(cond_right,False)
                self._remove_1(result[1])
        return self.ast

    def generate_error_random(self):
        random_loop_node_list = []
        for i in self.loop_node_list:
            n = random.randint(0,1)
            if n == 0:
                random_loop_node_list.append(i)
        ast = self.generate_error(random_loop_node_list)
        return ast


    def _remove_1(self,binary_op):
        c_generator = CGenerator()
        ast_str = c_generator.visit(self.ast)
        binary_op_str = c_generator.visit(binary_op)
        index = binary_op_str.index('1')
        binary_op_str_new = self._strip_bracket(binary_op_str[0:index-3]+binary_op_str[index+1:])
        ast_str = ast_str.replace(binary_op_str,binary_op_str_new)
        self.ast = self.parser.parse(ast_str)

    def _strip_bracket(self,str):
        if (str[0] == '(') & (str[-1] == ')'):
            str = str[1:-1]
            self._strip_bracket(str)
        return str

    def _format_1_expression(self,str):
        index = str.index('1')
        new_str = str[:index-3]+str[index+1:]
        print(new_str)
        pass

    def generate_error_default(self):
        ast = self.generate_error(self.loop_node_list)
        return ast

    def _dfs_find_constant_1(self,binary_op,is_Nested):
        if isinstance(binary_op.right,BinaryOp):
            self._dfs_find_constant_1(binary_op.right,True)
        elif isinstance(binary_op.right,Constant):
            if binary_op.right.value == '1':
                return (True,binary_op,is_Nested)
        return (False,None,False)