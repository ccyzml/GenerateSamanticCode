from error_models.if_error_model import *
from error_models.out_of_index_error_model import *
from error_models.block_error_model import *
from error_models.missing_1_error_model import *
from error_models.missing_break_error_model import *
from pycparser import CParser
from preproccess_code import PreproccessCode
class ErrorFactory:
    @staticmethod
    def generate_error_model(type,code=None,ast=None):
        if code:
            parser = CParser()
            ast = parser.parse(code)
        return {
            'if_error': IfErrorModel(ast),
            'out_of_index_error': OutOfIndexErrorModel(ast),
            'block_error': BlockErrorModel(ast),
            'missing_1_error': Missing1ErrorModel(ast),
            'missing_break_error': MissingBreakErrorModel(ast)
        }.get(type)
