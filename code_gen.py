from enum import Enum
from typing import List

PB_SIZE = 1000


def add_str(a1, a2, r):
    return '(ADD, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'

def mult_str(a1, a2, r):
    return '(MULT, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'

def sub_str(a1, a2, r):
    return '(SUB, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'

def eq_str(a1, a2, r):
    return '(EQ, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'

def lt_str(a1, a2, r):
    return '(LT, ' + str(a1) + ', ' + str(a2) + ', ' + str(r) + ')'

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


class CodeGen:

    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = parser.symbol_table.dict
        """
             {ID/KEYWORD lexeme: {SYMBOL_TABLE_KEYS.ADDRESS: address (int), ...}}
        """
        self.pb: List[str] = ['' for _ in range(PB_SIZE)]    # list of command strings in PB
        self.i = 0      # index used for pb
        self.ss: List[str] = []    # semantic stack (str)
        self.bs: List[int] = []    # break stack (int) contains pairs (Ai, bi) = (repeat_address, break_exists) for each repeat
        self.addr_counter = parser.addr_counter

        # init PB
        self.pb[0] = jp_str(1)
        self.i += 1

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
            if SYMBOL_TABLE_KEYS.ADDRESS in self.symbol_table[key] and\
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
