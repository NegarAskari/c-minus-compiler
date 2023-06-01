from code_gen import SYMBOL_TABLE_KEYS


class SemanticCheck:

    def __init__(self, parser):
        self.errors = []
        self.parser = parser
        self.void_flag = (False, '')
        self.scope_count = 0
        self.func_id = ''
        self.in_args = False
        self.define_id = ''
        self.num_arg = 0
        self.arg_id = ''
        self.in_params = False
        self.array_args = False
        self.count_repeat = 0
        self.current_type = ''
        self.last_type = ''
        self.check_type = False
        self.store_type = True
        self.param_id = ''

    def insert_void(self):
        self.void_flag = (True, self.parser.current_token[1])

    def funcion_declaration(self):
        self.void_flag = (False, '')

    def variable_declaration(self):
        if self.void_flag[0]:
            self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Illegal type of void for '{self.void_flag[1]}'.")
        self.void_flag = (False, '')

    def define(self):
        self.parser.symbol_table.dict[self.parser.current_token[1]][SYMBOL_TABLE_KEYS.SCOPE] = self.scope_count
        self.define_id = self.parser.current_token[1]
        self.param_id = self.parser.current_token[1]

    def scope_begin(self):
        self.scope_count += 1

    def scope_dec(self):
        self.scope_count -= 1
    
    def scope_end(self):
        st = self.parser.symbol_table.dict
        for id in st:
            if len(st[id]) > 0 and st[id][SYMBOL_TABLE_KEYS.SCOPE] == self.scope_count:
                st[id][SYMBOL_TABLE_KEYS.SCOPE] = -1
                st[id][SYMBOL_TABLE_KEYS.TYPE] = 'int'

        self.scope_count -= 1

    def check_defined(self):
        id = self.parser.current_token[1]
        if self.parser.symbol_table.dict[id][SYMBOL_TABLE_KEYS.SCOPE] == -1:
            self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! '{id}' is not defined.")
        if not self.in_args:
            self.func_id = id
        else:
            self.arg_id = id

    def set_func_id(self):
        if not self.in_params:
            self.func_id = self.parser.current_token[1]
    
    def param_in(self):
        self.in_params = True

    def param_out(self):
        self.in_params = False

    def array_param(self):
        self.parser.symbol_table.dict[self.func_id][SYMBOL_TABLE_KEYS.PARAMETERS].append('array')
        self.parser.symbol_table.dict[self.param_id][SYMBOL_TABLE_KEYS.TYPE] = 'array'

    def int_param(self):
        self.parser.symbol_table.dict[self.func_id][SYMBOL_TABLE_KEYS.PARAMETERS].append('int')

    def define_array(self):
        self.parser.symbol_table.dict[self.define_id][SYMBOL_TABLE_KEYS.TYPE] = 'array'

    def define_func(self):
        self.parser.symbol_table.dict[self.define_id][SYMBOL_TABLE_KEYS.TYPE] = 'func'

    def args_in(self):
        self.in_args = True
        self.num_arg = 0
    
    def args_out(self):
        params = self.parser.symbol_table.dict[self.func_id][SYMBOL_TABLE_KEYS.PARAMETERS]
        if len(params) > self.num_arg:
            self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Mismatch in numbers of arguments of '{self.func_id}'.")
        self.in_args = False

    def no_args(self):
        if len(self.parser.symbol_table.dict[self.func_id][SYMBOL_TABLE_KEYS.PARAMETERS]) > 0:
            self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Mismatch in numbers of arguments of '{self.func_id}'.")

    def check_arg(self):
        if self.in_args:
            params = self.parser.symbol_table.dict[self.func_id][SYMBOL_TABLE_KEYS.PARAMETERS]
            if len(params) <= self.num_arg:
                self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Mismatch in numbers of arguments of '{self.func_id}'.")
                return
            X = params[self.num_arg]
            Y = self.parser.symbol_table.dict[self.arg_id][SYMBOL_TABLE_KEYS.TYPE]
            if Y != X:
                self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Mismatch in type of argument {self.num_arg + 1} of '{self.func_id}'. Expected '{X}' but got '{Y}' instead.")
            self.num_arg += 1

    def check_arg_int(self):
        if self.in_args:
            params = self.parser.symbol_table.dict[self.func_id][SYMBOL_TABLE_KEYS.PARAMETERS]
            if len(params) <= self.num_arg:
                self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Mismatch in numbers of arguments of '{self.func_id}'.")
                return
            X = params[self.num_arg]
            Y = 'int'
            if Y != X:
                self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Mismatch in type of argument {self.num_arg + 1} of '{self.func_id}'. Expected '{X}' but got '{Y}' instead.")
            self.num_arg += 1

    def array_in(self):
        self.store_type = False
        if self.in_args:
            self.in_args = False
            self.array_args = True
    
    def array_out(self):
        self.store_type = True
        if self.array_args:
            self.array_args = False
            self.in_args = True

    def repeat(self):
        self.count_repeat += 1
    
    def until(self):
        self.count_repeat -= 1

    def check_break(self):
        if self.count_repeat == 0:
            self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! No 'repeat ... until' found for 'break'.")

    def match_type(self):
        self.check_type = True
        self.last_type = self.current_type

    def save_type(self):
        if not self.store_type:
            return
        self.current_type = self.parser.symbol_table.dict[self.parser.current_token[1]][SYMBOL_TABLE_KEYS.TYPE]
    
    def update_type(self):
        if not self.store_type:
            return
        if self.parser.current_token[1] == '[':
            self.current_type = 'int'
        if self.check_type:
            self.check_type = False
            if self.last_type != self.current_type:
                if self.errors[-1].startswith(f"#{self.parser.scanner.lineno}"):
                    return
                self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Type mismatch in operands, Got {self.current_type} instead of {self.last_type}.")

    def int_type(self):
        if not self.store_type:
            return
        self.current_type = 'int'
        if self.check_type:
            self.check_type = False
            if self.last_type != self.current_type:
                if self.errors[-1].startswith(f"#{self.parser.scanner.lineno}"):
                    return
                self.errors.append(f"#{self.parser.scanner.lineno}: Semantic Error! Type mismatch in operands, Got {self.current_type} instead of {self.last_type}.")