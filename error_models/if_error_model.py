from error_models.base_error_model import BaseErrorModel
from op_swap import get_random_op
class IfErrorModel(BaseErrorModel):
    def generate_error(self, if_body_list):
       for i in if_body_list:
           i.cond.op = get_random_op(i.cond.op)
           self._swap(i)
       return self.ast

    def generate_error_default(self):
        ast = self.generate_error(self.coll_if_body())
        return ast

    def _swap(self,if_body):
        cond = if_body.cond
        left = cond.left
        right = cond.right
        cond.left,cond.right = right,left