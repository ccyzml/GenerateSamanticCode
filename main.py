from  error_factory import *
from pycparser.c_generator import CGenerator


filePath = 'c_code_sample'
outPath = '/Users/zhangminglei/ErrorCode/'

out_of_index_error_model = ErrorFactory.generate_error_model('out_of_index_error',file_path = filePath)
ast = out_of_index_error_model.generate_error_default()
if_error_model = ErrorFactory.generate_error_model('if_error',ast = ast)
ast = if_error_model.generate_error_default()
block_error_model = ErrorFactory.generate_error_model('block_error',ast = ast)
ast = block_error_model.generate_error_default()
c_generator = CGenerator()
str = c_generator.visit(ast)
print(str)
