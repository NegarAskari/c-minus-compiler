from enum import Enum
from typing import List
from itertools import count

PB_SIZE = 1000


def add_str(a1, a2, r):
    return '(ADD, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'


def mult_str(a1, a2, r):
    return '(MULT, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'


def assign_str(a, r):
    return '(ASSIGN, ' + str(a) + ', ' + str(r) + ', )'


def jpf_str(a, l):
    return '(JPF, ' + str(a) + ', ' + str(l) + ', )'


def jp_str(l):
    return '(JP, ' + str(l) + ', , )'


def print_str(a):
    return '(PRINT, ' + str(a) + ', , )'


class SYMBOL_TABLE_KEYS(str, Enum):
    ADDRESS = 'address'
    ALLOCATED = 'allocated'
    # TYPE = 'type'

class FUNC_TABLE_KEYS(str, Enum):
    CALL_ADDRS = 'CALL_ADDRS'
    FUNC_ADDR = 'FUNC_ADDR'
    PARAMS_ADDRS = 'PARAMS_ADDRS'
    RETURN_ADDR = 'RETURN_ADDR'
    RETURN_VAL = 'RETURN_VAL'


class FuncTable:
    # func_id = str(self.symbol_table[func_name][SYMBOL_TABLE_KEYS.ADDRESS])

    def __init__(self):
        self.dict = dict()  # {func_id: {FUNC_TABLE_KEYS.CALL_ADDRS: [], FUNC_TABLE_KEYS.FUNC_ADDR: func_addr}}

    def exists(self, func_id):
        return func_id in self.dict

    def insert(self, func_id):
        self.dict[func_id] = {FUNC_TABLE_KEYS.CALL_ADDRS: [], FUNC_TABLE_KEYS.PARAMS_ADDRS: []}

    def append_call_addr(self, func_id, addr):
        self.dict[func_id][FUNC_TABLE_KEYS.CALL_ADDRS] = self.dict[func_id][FUNC_TABLE_KEYS.CALL_ADDRS] + [addr]

    def set_func_addr(self, func_id, func_addr):
        # set i in PB (start of func in PB)
        self.dict[func_id][FUNC_TABLE_KEYS.FUNC_ADDR] = func_addr

    def append_param_addr(self, func_id, param_addr):
        self.dict[func_id][FUNC_TABLE_KEYS.PARAMS_ADDRS] = self.dict[func_id][FUNC_TABLE_KEYS.PARAMS_ADDRS] + [param_addr]

    def set_return_addr(self, func_id, return_addr):
        self.dict[func_id][FUNC_TABLE_KEYS.RETURN_ADDR] = return_addr

    def set_return_val(self, func_id, return_val):
        self.dict[func_id][FUNC_TABLE_KEYS.RETURN_VAL] = return_val


class CodeGen:

    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = parser.symbol_table.dict
        """
             {ID/KEYWORD lexeme: {SYMBOL_TABLE_KEYS.ADDRESS: address (int), ...}}
        """
        self.pb: List[str] = ['' for _ in range(PB_SIZE)]  # list of command strings in PB
        self.i = 0  # index used for pb
        self.ss: List[str] = []  # semantic stack (str)
        self.bs: List[int] = []  # break stack (int)
        self.addr_counter = parser.addr_counter

        self.func_table = FuncTable()
        self.func_id = []   # func_ids stack
        self.arg_count = 0

        # init PB
        self.pb[0] = jp_str(1)
        self.i += 1

    def func_declare(self):
        self.func_id.append(self.ss[-1])
        self.func_table.insert(self.func_id[-1])
        self.func_table.set_func_addr(self.func_id[-1], self.i)
        self.func_table.set_return_addr(self.func_id[-1], next(self.addr_counter))
        self.func_table.set_return_val(self.func_id[-1], next(self.addr_counter))
        if self.is_main():
            self.pb[0] = jp_str(self.i)
        self.ss.pop()

    def is_main(self):
        return ('main' in self.symbol_table) and \
            (str(self.symbol_table['main'][SYMBOL_TABLE_KEYS.ADDRESS]) == self.func_id[-1])

    def add_param(self):
        param_addr = self.ss[-1]
        self.func_table.append_param_addr(self.func_id[-1], param_addr)
        self.ss.pop()

    def pop_func_id(self):
        self.func_id.pop()

    def init_call(self):
        if self.func_id[-1] == self.ss[-1]:
            self.pb[self.i] = jp_str('#1000')
            self.i += 1
        self.func_id.append(self.ss[-1])
        self.func_table.append_call_addr(self.func_id[-1], self.i)
        self.ss.pop()
        self.arg_count = 0

    def call_after_args(self):
        self.pb[self.i] = assign_str('#' + str(self.i + 2), self.func_table.dict[self.func_id[-1]][FUNC_TABLE_KEYS.RETURN_ADDR])
        self.i += 1
        self.pb[self.i] = jp_str(self.func_table.dict[self.func_id[-1]][FUNC_TABLE_KEYS.FUNC_ADDR])
        self.i += 1
        self.ss.append(str(self.func_table.dict[self.func_id[-1]][FUNC_TABLE_KEYS.RETURN_VAL]))
        self.pop_func_id()

    def add_arg(self):
        expression = self.ss[-1]
        self.pb[self.i] = assign_str(expression,
                                     self.func_table.dict[self.func_id[-1]][FUNC_TABLE_KEYS.PARAMS_ADDRS][self.arg_count])
        self.i += 1
        self.arg_count += 1
        self.ss.pop()

    def return_(self):
        if not self.is_main():
            self.pb[self.i] = jp_str('@' + str(self.func_table.dict[self.func_id[-1]][FUNC_TABLE_KEYS.RETURN_ADDR]))
            self.i += 1

    def return_val(self):
        self.pb[self.i] = assign_str(self.ss[-1], self.func_table.dict[self.func_id[-1]][FUNC_TABLE_KEYS.RETURN_VAL])
        self.i += 1
        self.ss.pop()
        self.return_()


    def pid(self):
        id_lexeme = self.parser.current_token[1]
        p = self.symbol_table[id_lexeme][SYMBOL_TABLE_KEYS.ADDRESS]
        self.ss.append(str(p))

    def pnum(self):
        num_lexeme = self.parser.current_token[1]
        self.ss.append(str('#' + str(num_lexeme)))

    def allocate_var(self):
        for key in self.symbol_table:
            if SYMBOL_TABLE_KEYS.ADDRESS in self.symbol_table[key] and \
                    self.symbol_table[key][SYMBOL_TABLE_KEYS.ADDRESS] == int(self.ss[-1]):
                self.symbol_table[key][SYMBOL_TABLE_KEYS.ALLOCATED] = True
        self.pb[self.i] = assign_str('#0', self.ss[-1])
        self.i += 1
        self.ss.pop()

    def allocate_var_assign(self):
        already_allocated = False
        for key in self.symbol_table:
            if SYMBOL_TABLE_KEYS.ADDRESS in self.symbol_table[key] and \
                    self.symbol_table[key][SYMBOL_TABLE_KEYS.ADDRESS] == int(self.ss[-1]):
                if self.symbol_table[key][SYMBOL_TABLE_KEYS.ALLOCATED]:
                    already_allocated = True
                else:
                    self.symbol_table[key][SYMBOL_TABLE_KEYS.ALLOCATED] = True
        if not already_allocated:
            self.pb[self.i] = assign_str('#0', self.ss[-1])
            self.i += 1

    def allocate_array(self):
        for key in self.symbol_table:
            if SYMBOL_TABLE_KEYS.ADDRESS in self.symbol_table[key] and \
                    self.symbol_table[key][SYMBOL_TABLE_KEYS.ADDRESS] == int(self.ss[-2]):
                self.symbol_table[key][SYMBOL_TABLE_KEYS.ALLOCATED] = True
        self.pb[self.i] = assign_str('#0', self.ss[-2])
        arr_len = int(self.ss[-1][1:])
        for _ in range(arr_len - 1):
            next(self.addr_counter)
            # self.pb[self.i] = assign_str('#0', next(self.addr_counter))
            # self.i += 1
        self.ss.pop()
        self.ss.pop()
        self.i += 1

    def save(self):
        self.ss.append(str(self.i))
        self.i += 1

    def jpf_save(self):
        self.pb[int(self.ss[-1])] = jpf_str(self.ss[-2], self.i + 1)
        self.ss.pop()
        self.ss.pop()
        self.ss.append(str(self.i))
        self.i += 1

    def jp(self):
        self.pb[int(self.ss[-1])] = jp_str(self.i)
        self.ss.pop()

    def save_break(self):
        break_count = self.bs.pop()
        self.bs.append(self.i)
        self.bs.append(break_count + 1)
        self.i += 1

    def init_repeat(self):
        self.ss.append(str(self.i))
        # for break
        self.bs.append(0)

    def until(self):
        self.pb[self.i] = jpf_str(self.ss[-1], self.ss[-2])
        self.i += 1
        self.ss.pop()
        self.ss.pop()
        # for break
        break_count = self.bs.pop()
        for _ in range(break_count):
            a = self.bs.pop()
            self.pb[a] = jp_str(self.i)

    def offset(self):
        t = next(self.addr_counter)
        self.pb[self.i] = mult_str('#4', self.ss[-1], t)
        self.pb[self.i + 1] = add_str(str('#' + self.ss[-2]), t, t)
        self.ss.pop()
        self.ss.pop()
        self.ss.append(str('@' + str(t)))
        self.i += 2

    def assign(self):
        self.pb[self.i] = assign_str(self.ss[-1], self.ss[-2])
        self.i += 1
        self.ss.pop()

    def mult(self):
        t = next(self.addr_counter)
        self.pb[self.i] = mult_str(self.ss[-2], self.ss[-1], t)
        self.i += 1
        self.ss.pop()
        self.ss.pop()
        self.ss.append(str(t))

    def push_add(self):
        self.ss.append('ADD')

    def push_sub(self):
        self.ss.append('SUB')

    def push_lt(self):
        self.ss.append('LT')

    def push_eq(self):
        self.ss.append('EQ')

    def op(self):
        t = next(self.addr_counter)
        self.pb[self.i] = '(' + self.ss[-2] + ', ' + self.ss[-3] + ', ' + self.ss[-1] + ', ' + str(t) + ')'
        self.ss.pop()
        self.ss.pop()
        self.ss.pop()
        self.ss.append(str(t))
        self.i += 1

    def pop(self):
        self.ss.pop()

    def print(self):
        self.pb[self.i] = print_str(self.ss[-1])
        self.ss.pop()
        self.i += 1
