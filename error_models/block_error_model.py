from error_models.base_error_model import BaseErrorModel
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment

class BlockErrorModel(BaseErrorModel):
    def __init__(self,ast):
        self.assignmentList = []
        super().__init__(ast)


    def generate_error(self, block_items):
        for item in block_items:
            self.find_assignment_in_block(item)
        return self.ast

    def generate_error_default(self):
        ast = self.generate_error(self.coll_block_items())
        return ast

    def find_assignment_in_block(self,node):
        self._dfs_assignment(node)
        if (len(self.assignmentList) > 2):
            print('find injection')
            self._generate_variable_chaos()
            self.assignmentList.clear()

    def _generate_variable_chaos(self):
        temp_assignment = self.assignmentList[0]
        self.assignmentList.remove(temp_assignment)
        temp_right = temp_assignment.rvalue
        for assignment in self.assignmentList:
            assignment.lvalue = temp_right
            temp_right = assignment.rvalue
        temp_assignment.lvalue = temp_right



    def _dfs_assignment(self, node):
        if isinstance(node, Node):
            if isinstance(node, Assignment):
                self.assignmentList.append(node)
            nodes = node.children()
            if nodes:
                for i in nodes:
                    self._dfs_assignment(i)
        elif isinstance(node, list):
            for i in node:
                self._dfs_assignment(i)
