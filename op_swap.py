import random
def get_random_op(old_op):
    ops = ['==','<','<=','>=','>']
    ops.remove(old_op)
    return ops[random.randint(0,len(ops)-1)]