from  error_factory import *
from pycparser.c_generator import CGenerator
from preproccess_code import PreproccessCode


filePath = 'c_code_bubble_sort'
outPath = '/Users/zhangminglei/ErrorCode/'

pc = PreproccessCode(filePath)
'''
out_of_index_error_model = ErrorFactory.generate_error_model('out_of_index_error',code = pc.pure_code)
ast = out_of_index_error_model.generate_error_random()
if_error_model = ErrorFactory.generate_error_model('if_error',ast = ast)
ast = if_error_model.generate_error_random()
block_error_model = ErrorFactory.generate_error_model('block_error',ast = ast)
ast = block_error_model.generate_error_random()
missing_1_error_model = ErrorFactory.generate_error_model('missing_1_error',ast = ast)
ast = missing_1_error_model.generate_error_random()
'''
missing_break_error_model = ErrorFactory.generate_error_model('missing_break_error',code = pc.pure_code)
ast = missing_break_error_model.generate_error_default()
c_generator = CGenerator()
str = c_generator.visit(ast)
code = pc.head_code+str
print(code)

