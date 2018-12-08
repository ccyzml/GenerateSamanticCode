from error_models.base_error_model import *
from pycparser.c_ast import Switch,Case,Break
import random
class MissingBreakErrorModel(BaseErrorModel):
    def __init__(self,ast):
        super().__init__(ast)
        self.switch_node_list = []
        self._coll_switch_node()

    def _coll_switch_node(self):
        for node in self.node_list:
            if isinstance(node, Switch):
                self.switch_node_list.append(node)

    def generate_error(self,error_list,**args):
        for node in error_list:
            self._remove_case_break(node)
        return self.ast

    def _remove_case_break(self,switch_node):
        block = switch_node.stmt.block_items
        for case_node in block:
            if isinstance(case_node,Case):
                case_node_stmts = case_node.stmts
                if isinstance(case_node_stmts[-1],Break):
                    break_node = case_node_stmts[-1]
                    case_node_stmts.remove(break_node)
        pass

    def generate_error_default(self):
        ast = self.generate_error(self.switch_node_list)
        return ast

    def generate_error_random(self):
        random_switch_node_list = []
        for i in self.switch_node_list:
            n = random.randint(0, 1)
            if n == 0:
                random_switch_node_list.append(i)
        ast = self.generate_error(random_switch_node_list)
        return ast