from pycparser import c_parser, c_ast, parse_file,c_generator
from pycparser.c_ast import Decl,For,While,DoWhile,Node,If,FuncDef,Compound,Assignment
import time


class ErrorGenerator:
    def __init__(self, filePath):
        self.codeContentList = self._format_file(filePath)
        self.declList = []
        self.forList = []
        self.ifList = []
        self.funDefList = []
        self.blockItemList = []
        self.ast = parse_file(filePath)
        self._coll_nodes()


    def generate_out_of_index_error(self,loop_body_list):
        for item in loop_body_list:
            if isinstance(item, For):
                forStr = self._translate_for_loop_str(item)
                loc = self._find_line_loc(forStr)
                errorForStr = self._generate_error_for_str(item)
                self._replaceCode(loc, forStr, errorForStr)
        print(self.codeContentList)


    def generate_swap_variable_error(self,block_item_list):
        for item in block_item_list:
            variables = self._coll_variable_in_block(item)
            correct_variable_list =[]
            error_variable_list = self._generate_confuse_variables_list(variables)
            for variable in variables:
                correct_variable_list.append(self._translate_variable_swap_str(variable))
            for i in range(len(correct_variable_list)):
                loc = self._find_line_loc(correct_variable_list[i])
                print(loc)
                self._replaceCode(loc,correct_variable_list[i],error_variable_list[i])

    def _translate_variable_swap_str(self,variable):
        str = variable.lvalue.name+variable.op+variable.rvalue.name
        return str

    def _generate_confuse_variables_list(self,variables):
        confused_str_list = []
        if len(variables) > 1:
            rvalue = variables[-1].rvalue
            for variable in variables:
                str = variable.lvalue.name + variable.op + rvalue.name
                confused_str_list.append(str)
                rvalue = variable.rvalue
        return confused_str_list



    def _coll_variable_in_block(self,block_items):
        variables = []
        for i in block_items:
            if isinstance(i,Assignment):
                variables.append(i)
        return variables

    def _dfs(self,node):
        if isinstance(node,Node):
            if isinstance(node, For):
                self.forList.append(node)
            elif isinstance(node, Decl):
                self.declList.append(node)
            elif isinstance(node, If):
                self.ifList.append(node)
            elif isinstance(node,FuncDef):
                self.funDefList.append(node)
            elif isinstance(node,Compound):
                self.blockItemList.append(node.block_items)
            nodes = node.children()
            if nodes:
                for i in nodes:
                    self._dfs(i)
        elif isinstance(node, list):
            for i in node:
                self._dfs(i)

    def generate_if_error(self,if_body_list):
        for i in if_body_list:
            ifStr = self._translate_if_str(i)
            loc = self._find_line_loc(ifStr)
            self._replaceCode(loc,ifStr,self._generate_error_if_str(i))


    def generate_variable_error(self,variable_list):
        print('######working')



    def _replaceCode(self,loc, correct_code, error_code):
        for i in loc:
            self.codeContentList[i] = self.codeContentList[i].replace(correct_code, error_code)

    def write(self,dirPath):
        f = open(dirPath + str(time.time()) + '.cpp', 'a')
        f.writelines(self.codeContentList)

    def _translate_if_str(self,ifBody):
        cond = ifBody.cond
        ifStr = cond.left.name+cond.op+cond.right.name
        return ifStr

    def _generate_error_if_str(self, ifBody):
        cond = ifBody.cond
        ifStr = cond.right.name + cond.op + cond.left.name
        return ifStr

    def _translate_for_loop_str(self,forBody):
        init = forBody.init
        cond = forBody.cond
        next = forBody.next
        forStr = 'for(' + init.lvalue.name + init.op + init.rvalue.value + ';' \
                 + cond.left.name + cond.op + cond.right.value + ';' \
                 + next.op.replace('p', next.expr.name) + ')'
        return forStr

    def _generate_error_for_str(self,forBody):
        init = forBody.init
        cond = forBody.cond
        next = forBody.next
        error_range = int(cond.right.value) + 1
        forStr = 'for(' + init.lvalue.name + init.op + init.rvalue.value + ';' \
                 + cond.left.name + cond.op + str(error_range) + ';' \
                 + next.op.replace('p', next.expr.name) + ')'
        return forStr

    def _find_line_loc(self, content):
        lineLoc = []
        i = 0
        for code in self.codeContentList:
            if content in code:
                lineLoc.append(i)
            i += 1
        return lineLoc

    def _format_file(self,file_path):
        codeContentList = []
        file = open(file_path)
        for line in file:
            codeContentList.append(line)
        return codeContentList;

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

    def _coll_nodes(self):
        for i in self.ast.children():
            self._dfs(i[1])

    def show_ast(self):
        print(self.ast.children())