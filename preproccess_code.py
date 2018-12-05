#去除头文件和comments
class PreproccessCode:

    def __init__(self, code):
        self._code = code
        self._remove_comments()
        self._head_code = self._stash_head_code()
        self._pure_code = self._code.replace(self._head_code,'')

    def _remove_comments(self):
        code_list = self._code.split('\n')
        code = ''
        for line in code_list:
            if '//' in line:
                line = line.split('//')[0]
            if line:
                code += line+'\n'
        self._code = code

    def _stash_head_code(self):
        code_list = self._code.split('\n')
        head_code = ''
        for line in code_list:
            if '#' in line:
               head_code += line+'\n'
            else:
                break
        return head_code

    @property
    def head_code(self):
        return self._head_code

    @property
    def pure_code(self):
        return self._pure_code