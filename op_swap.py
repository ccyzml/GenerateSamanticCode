import random
def get_error_op(old_op):
    if old_op == '<':
        return '<='
    elif old_op == '>':
        return '>='
    elif old_op == '==':
        return '=='
    elif old_op == '>=':
        return '>'
    elif old_op == '<=':
        return '<'
    return '=='