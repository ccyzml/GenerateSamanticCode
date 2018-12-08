from error_models.base_error_model import BaseErrorModel
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment
from pycparser.c_generator import CGenerator
import random

class BlockErrorModel(BaseErrorModel):
    def __init__(self,ast):
        super().__init__(ast)
        self.block_item_list = []
        self.assignment_list = []
        self._coll_block_items()


    def generate_error(self, block_items):
        for item in block_items:
            result = self._find_injection_point(item)
            if result[0]:
                self._generate_swap_error(result[1],item)
        return self.ast

    def _generate_swap_error(self,swap_list,block_item):
        block_item.remove(swap_list[0])
        assignment_1 = swap_list[1]
        assignment_2 = swap_list[2]
        assignment_2.rvalue = assignment_1.lvalue

    def generate_error_default(self):
        ast = self.generate_error(self.block_item_list)
        return ast

    def generate_error_random(self):
        random_block_item_list = []
        for i in self.block_item_list:
            n = random.randint(0,1)
            if n == 0:
                random_block_item_list.append(i)
        ast = self.generate_error(random_block_item_list)
        return ast


    def _coll_block_items(self):
        for node in self.node_list:
            if isinstance(node, Compound):
             self.block_item_list.append(node.block_items)

    def _find_injection_point(self,block):
        n = 0
        m = False
        swap_list = []
        for i in block:
            if (isinstance(i,Decl) | isinstance(i,Assignment)) & (not m):
                n += 1
                m = True
                swap_list.append(i)
            elif isinstance(i,Assignment) & m:
                n += 1
                swap_list.append(i)
            else:
                m = False
                swap_list.clear()
                n = 0
            if n == 3:
                if(self._check_is_swap(swap_list)):
                    return (True,swap_list)
                else:
                    swap_list.clear()
                    m = False
                    n = 0
        return (False,[])


    def _check_is_swap(self, block_list):
        c_generate = CGenerator()
        node_0 = block_list[0]
        node_0_left,node_0_right = c_generate.visit(node_0).split('=')
        if isinstance(node_0,Decl):
            node_0_left = node_0_left.split(' ')[1]
        assignment_1 = block_list[1]
        assignment_2 = block_list[2]
        assignment_1_code = c_generate.visit(assignment_1)
        assignment_2_code = c_generate.visit(assignment_2)
        print(assignment_1_code)
        assignment_1_code_left,assignment_1_code_right = assignment_1_code.split('=')
        assignment_2_code_left, assignment_2_code_right = assignment_2_code.split('=')
        if (self.check_equal(node_0_right, assignment_1_code_left) & self.check_equal(assignment_1_code_right, assignment_2_code_left) & self.check_equal(assignment_2_code_right, node_0_left)):
            return True
        return False

    def check_equal(self, left, right):
        r = (left.strip() == right.strip())
        return r
