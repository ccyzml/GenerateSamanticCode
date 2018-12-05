from error_models.if_error_model import *
from error_models.out_of_index_error_model import *
from error_models.block_error_model import *
from pycparser import CParser
from preproccess_code import PreproccessCode
class ErrorFactory:
    @staticmethod
    def generate_error_model(type,file_path=None,ast=None):
        if file_path:
            code_list = open(file_path).readlines()  # need preproccessing
            code = ''
            for line in code_list:
                code += line
            parser = CParser()
            pc = PreproccessCode(code)
            print(pc.pure_code)
            ast = parser.parse(pc.pure_code)
        return {
            'if_error': IfErrorModel(ast),
            'out_of_index_error': OutOfIndexErrorModel(ast),
            'block_error': BlockErrorModel(ast)
        }.get(type)