from anytree import Node
from scanner import *
from code_gen import *


first_dict = {'Declaration-list': ['int', 'void'], 'Var-declaration-prime': [';', '['], 'Fun-declaration-prime': ['('],
              'Type-specifier': ['int', 'void'], 'Params': ['int', 'void'], 'Param-list': [','], 'Param-prime': ['['],
              'Compound-stmt': ['{'], 'Expression-stmt': ['break', ';', 'ID', '(', 'NUM'], 'Selection-stmt': ['if'],
              'Iteration-stmt': ['repeat'], 'Return-stmt': ['return'], 'Return-stmt-prime': [';', 'ID', '(', 'NUM'],
              'Expression': ['ID', '(', 'NUM'], 'B': ['='], 'H': ['='], 'C': ['<', '=='], 'Relop': ['<', '=='],
              'D': ['+', '-'], 'Addop': ['+', '-'], 'G': ['*'], 'Factor': ['(', 'ID', 'NUM'],
              'Var-call-prime': ['(', '['], 'Var-prime': ['['], 'Factor-prime': ['('], 'Factor-zegond': ['(', 'NUM'],
              'Args': ['ID', '(', 'NUM'], 'Arg-list-prime': [','], 'Declaration-initial': ['int', 'void'],
              'Declaration-prime': ['(', ';', '['], 'Term': ['(', 'ID', 'NUM'], 'Term-prime': ['(', '*'],
              'Term-zegond': ['(', 'NUM'], 'Declaration': ['int', 'void'], 'Param': ['int', 'void'],
              'Additive-expression': ['(', 'ID', 'NUM'], 'Additive-expression-zegond': ['(', 'NUM'],
              'Simple-expression-zegond': ['(', 'NUM'], 'Additive-expression-prime': ['(', '*', '+', '-'],
              'Program': ['int', 'void'], 'Simple-expression-prime': ['(', '*', '+', '-', '<', '=='],
              'Arg-list': ['ID', '(', 'NUM'],
              'Statement': ['break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', 'output'],
              'Statement-list': ['break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', 'output']}
follow_dict = {'Program': ['$'],
               'Declaration-list': ['break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', '}', 'repeat', '$', 'output'],
               'Declaration': ['int', 'void', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '$'],
               'Declaration-initial': ['[', '(', ';', ',', ')'],
               'Declaration-prime': ['int', 'void', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '$'],
               'Var-declaration-prime': ['int', 'void', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat',
                                         '$'],
               'Fun-declaration-prime': ['int', 'void', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat',
                                         '$'], 'Type-specifier': ['ID'], 'Params': [')'], 'Param-list': [')'],
               'Param': [',', ')'], 'Param-prime': [',', ')'],
               'Compound-stmt': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', 'int',
                                 'void', '$', '}'], 'Statement-list': ['}'],
               'Statement': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '}', 'output'],
               'Expression-stmt': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '}'],
               'Selection-stmt': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '}'],
               'Iteration-stmt': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '}'],
               'Return-stmt': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat', '}'],
               'Return-stmt-prime': ['until', 'else', 'break', ';', 'ID', '(', 'NUM', 'if', 'return', '{', 'repeat',
                                     '}'], 'Expression': [',', ')', ']', ';'], 'B': [',', ')', ']', ';'],
               'H': [',', ')', ']', ';'], 'Simple-expression-zegond': [',', ')', ']', ';'],
               'Simple-expression-prime': [',', ')', ']', ';'], 'C': [',', ')', ']', ';'], 'Relop': ['(', 'ID', 'NUM'],
               'Additive-expression': [',', ')', ']', ';'],
               'Additive-expression-prime': ['<', '==', ',', ')', ']', ';'],
               'Additive-expression-zegond': ['<', '==', ',', ')', ']', ';'], 'D': ['<', '==', ',', ')', ']', ';'],
               'Addop': ['(', 'ID', 'NUM'], 'Term': ['+', '-', '<', '==', ',', ')', ']', ';'],
               'Term-prime': ['+', '-', '<', '==', ',', ')', ']', ';'],
               'Term-zegond': ['+', '-', '<', '==', ',', ')', ']', ';'], 'G': ['+', '-', '<', '==', ',', ')', ']', ';'],
               'Factor': ['*', '+', '-', '<', '==', ',', ')', ']', ';'],
               'Var-call-prime': ['*', '+', '-', '<', '==', ',', ')', ']', ';'],
               'Var-prime': ['*', '+', '-', '<', '==', ',', ')', ']', ';'],
               'Factor-prime': ['*', '+', '-', '<', '==', ',', ')', ']', ';'],
               'Factor-zegond': ['*', '+', '-', '<', '==', ',', ')', ']', ';'], 'Args': [')'], 'Arg-list': [')'],
               'Arg-list-prime': [')']}


class SymbolTable:
    def __init__(self, addr_counter):
        self.dict = OrderedDict()  # {ID/KEYWORD: dict()}
        self.addr_counter = addr_counter

    def initialize_with_keywords(self):
        for key in ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void', 'output']:
            self.dict[key] = dict()

    def exists(self, name):
        return name in self.dict

    def insert(self, name):
        self.dict[name] = {SYMBOL_TABLE_KEYS.ADDRESS: next(self.addr_counter)}
                           # SYMBOL_TABLE_KEYS.ALLOCATED: False}


class Parser:
    def __init__(self, input_file):
        self.stack = []
        self.addr_counter = count(start=PB_SIZE, step=4)
        self.symbol_table = SymbolTable(self.addr_counter)
        self.scanner = Scanner(input_file, self.symbol_table)
        self.grammar = {'First': first_dict, 'Follow': follow_dict}
        self.errors = []
        self.code_gen = CodeGen(parser=self)

    def next_token(self):
        self.current_token = self.scanner.get_next_token()
        self.terminal = self.current_token[1]
        if self.current_token[0] == 'NUM' or self.current_token[0] == 'ID':  # get terminal form
            self.terminal = self.current_token[0]

    def add_error(self, error):
        self.errors.append(f"#{self.scanner.lineno} : syntax error, {error}")

    def generate_tree(self):
        self.next_token()
        self.Program()
        while len(self.stack):

            popped = self.stack.pop()
            if callable(popped):

                #print(self.code_gen.func_id)

                # CodeGen
                popped()
            else:
                edge, parent = popped
                if callable(edge):
                    edge(parent)
                else:
                    if edge == self.terminal:
                        lexeme = '$' if self.terminal == '$' else f"({self.current_token[0]}, {self.current_token[1]})"
                        Node(lexeme, parent)
                        self.next_token()
                    else:
                        if self.terminal == '$':
                            self.add_error("Unexpected EOF")
                            self.stack = []
                        else:
                            self.add_error(f"missing {edge}")

    def error_handler(self, name, method, node):
        if self.terminal in self.grammar['Follow'][name]:
            self.add_error(f"missing {name}")
            node.parent = None
        else:
            if self.terminal == '$':
                self.stack = [('', '')]
                node.parent = None
            else:
                self.add_error(f"illegal {self.terminal}")
                self.next_token()
                parent = node.parent
                node.parent = None
                self.stack.append((method, parent))

    def Program(self):
        self.root = Node("Program")
        if self.terminal in self.grammar['First']['Declaration-list'] or self.terminal in self.grammar['Follow'][
            'Program']:
            self.stack.append(('$', self.root))
            self.stack.append((self.Declaration_list, self.root))
        else:
            self.error_handler('Program', self.Program, self.root)

    def Declaration_list(self, parent):
        node = Node('Declaration-list', parent)
        if self.terminal in self.grammar['First']['Declaration']:
            self.stack.append((self.Declaration_list, node))
            self.stack.append((self.Declaration, node))
        elif self.terminal in self.grammar['Follow']['Declaration-list']:
            Node('epsilon', node)
        else:
            self.error_handler('Declaration-list', self.Declaration_list, node)

    def Declaration(self, parent):
        node = Node('Declaration', parent)
        if self.terminal in self.grammar['First']['Declaration-initial']:
            self.stack.append((self.Declaration_prime, node))
            self.stack.append((self.Declaration_initial, node))
        else:
            self.error_handler('Declaration', self.Declaration, node)

    def Declaration_initial(self, parent):
        node = Node('Declaration-initial', parent)
        if self.terminal in self.grammar['First']['Type-specifier']:
            self.stack.append(('ID', node))
            self.stack.append(self.code_gen.pid)
            self.stack.append((self.Type_specifier, node))
        else:
            self.error_handler('Declaration-initial', self.Declaration_initial, node)

    def Declaration_prime(self, parent):
        node = Node('Declaration-prime', parent)
        if self.terminal in self.grammar['First']['Fun-declaration-prime']:
            # self.stack.append(self.code_gen.pop)
            self.stack.append((self.Fun_declaration_prime, node))
            # self.stack.append(self.code_gen.pop)
            self.stack.append(self.code_gen.func_declare)
        elif self.terminal in self.grammar['First']['Var-declaration-prime']:
            self.stack.append((self.Var_declaration_prime, node))
        else:
            self.error_handler('Declaration-prime', self.Declaration_prime, node)

    def Var_declaration_prime(self, parent):
        node = Node('Var-declaration-prime', parent)
        if self.terminal == ';':
            self.stack.append(self.code_gen.allocate_var)
            self.stack.append((';', node))
            self.stack.append(self.code_gen.add_local_var)
        elif self.terminal == '[':
            self.stack.append(self.code_gen.allocate_array)
            self.stack.append((';', node))
            self.stack.append((']', node))
            self.stack.append(('NUM', node))
            self.stack.append(self.code_gen.pnum)
            self.stack.append(('[', node))
            self.stack.append(self.code_gen.add_local_arr)
        else:
            self.error_handler('Var-declaration-prime', self.Var_declaration_prime, node)

    def Fun_declaration_prime(self, parent):
        node = Node('Fun-declaration-prime', parent)
        if self.terminal == '(':
            self.stack.append(self.code_gen.pop_func_id)
            self.stack.append(self.code_gen.ret_jump)
            self.stack.append((self.Compound_stmt, node))
            self.stack.append((')', node))
            self.stack.append((self.Params, node))
            self.stack.append(('(', node))
        else:
            self.error_handler('Fun-declaration-prime', self.Fun_declaration_prime, node)

    def Type_specifier(self, parent):
        node = Node('Type-specifier', parent)
        if self.terminal == 'int':
            self.stack.append(('int', node))
        elif self.terminal == 'void':
            self.stack.append(('void', node))
        else:
            self.error_handler('Type-specifier', self.Type_specifier, node)

    def Params(self, parent):
        node = Node('Params', parent)
        if self.terminal == 'int':
            self.stack.append((self.Param_list, node))
            self.stack.append((self.Param_prime, node))
            self.stack.append(('ID', node))
            self.stack.append(self.code_gen.pid)
            self.stack.append(('int', node))
        elif self.terminal == 'void':
            self.stack.append(('void', node))
        else:
            self.error_handler('Params', self.Params, node)

    def Param_list(self, parent):
        node = Node('Param-list', parent)
        if self.terminal == ',':
            self.stack.append((self.Param_list, node))
            self.stack.append((self.Param, node))
            self.stack.append((',', node))
        elif self.terminal in self.grammar['Follow']['Param-list']:
            Node('epsilon', node)
        else:
            self.error_handler('Param-list', self.Param_list, node)

    def Param(self, parent):
        node = Node('Param', parent)
        if self.terminal in self.grammar['First']['Declaration-initial']:
            self.stack.append((self.Param_prime, node))
            self.stack.append((self.Declaration_initial, node))
        else:
            self.error_handler('Param', self.Param, node)

    def Param_prime(self, parent):
        node = Node('Param-prime', parent)
        if self.terminal == '[':
            self.stack.append((']', node))
            self.stack.append(('[', node))
            self.stack.append(self.code_gen.add_param_arr)
        elif self.terminal in self.grammar['Follow']['Param-prime']:
            Node('epsilon', node)
            self.stack.append(self.code_gen.add_param_var)
        else:
            self.error_handler('Param-prime', self.Param_prime, node)

    def Compound_stmt(self, parent):
        node = Node('Compound-stmt', parent)
        if self.terminal == '{':
            self.stack.append(('}', node))
            self.stack.append((self.Statement_list, node))
            self.stack.append((self.Declaration_list, node))
            self.stack.append(('{', node))
        else:
            self.error_handler('Compound-stmt', self.Compound_stmt, node)

    def Statement_list(self, parent):
        node = Node('Statement-list', parent)
        if self.terminal in self.grammar['First']['Statement']:
            self.stack.append((self.Statement_list, node))
            self.stack.append((self.Statement, node))
        elif self.terminal in self.grammar['Follow']['Statement-list']:
            Node('epsilon', node)
        else:
            self.error_handler('Statement-list', self.Statement_list, node)

    def Statement(self, parent):
        node = Node('Statement', parent)
        if self.terminal == 'output':
            self.stack.append((';', node))
            self.stack.append((')', node))
            self.stack.append(self.code_gen.print)
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
            self.stack.append(('output', node))
        elif self.terminal in self.grammar['First']['Expression-stmt']:
            self.stack.append((self.Expression_stmt, node))
        elif self.terminal in self.grammar['First']['Compound-stmt']:
            self.stack.append((self.Compound_stmt, node))
        elif self.terminal in self.grammar['First']['Selection-stmt']:
            self.stack.append((self.Selection_stmt, node))
        elif self.terminal in self.grammar['First']['Iteration-stmt']:
            self.stack.append((self.Iteration_stmt, node))
        elif self.terminal in self.grammar['First']['Return-stmt']:
            self.stack.append((self.Return_stmt, node))
        else:
            self.error_handler('Statement', self.Statement, node)

    def Expression_stmt(self, parent):
        node = Node('Expression-stmt', parent)
        if self.terminal in self.grammar['First']['Expression']:
            self.stack.append(self.code_gen.pop)
            self.stack.append((';', node))
            self.stack.append((self.Expression, node))
        elif self.terminal == 'break':
            self.stack.append((';', node))
            self.stack.append(self.code_gen.save_break)
            self.stack.append(('break', node))
        elif self.terminal == ';':
            self.stack.append((';', node))
        else:
            self.error_handler('Expression-stmt', self.Expression_stmt, node)

    def Selection_stmt(self, parent):
        node = Node('Selection-stmt', parent)
        if self.terminal == 'if':
            self.stack.append(self.code_gen.jp)
            self.stack.append((self.Statement, node))
            self.stack.append(self.code_gen.jpf_save)
            self.stack.append(('else', node))
            self.stack.append((self.Statement, node))
            self.stack.append((')', node))
            self.stack.append(self.code_gen.save)
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
            self.stack.append(('if', node))
        else:
            self.error_handler('Selection-stmt', self.Selection_stmt, node)

    def Iteration_stmt(self, parent):
        node = Node('Iteration-stmt', parent)
        if self.terminal == 'repeat':
            self.stack.append((')', node))
            self.stack.append(self.code_gen.until)
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
            self.stack.append(('until', node))
            self.stack.append((self.Statement, node))
            self.stack.append(self.code_gen.init_repeat)
            self.stack.append(('repeat', node))
        else:
            self.error_handler('Iteration-stmt', self.Iteration_stmt, node)

    def Return_stmt(self, parent):
        node = Node('Return-stmt', parent)
        if self.terminal == 'return':
            self.stack.append((self.Return_stmt_prime, node))
            self.stack.append(('return', node))
        else:
            self.error_handler('Return-stmt', self.Return_stmt, node)

    def Return_stmt_prime(self, parent):
        node = Node('Return-stmt-prime', parent)
        if self.terminal in self.grammar['First']['Expression']:
            self.stack.append((';', node))
            self.stack.append(self.code_gen.return_val)
            self.stack.append((self.Expression, node))
        elif self.terminal == ';':
            self.stack.append(self.code_gen.ret_jump)
            self.stack.append((';', node))
        else:
            self.error_handler('Return-stmt-prime', self.Return_stmt_prime, node)

    def Expression(self, parent):
        node = Node('Expression', parent)
        if self.terminal in self.grammar['First']['Simple-expression-zegond']:
            self.stack.append((self.Simple_expression_zegond, node))
        elif self.terminal == 'ID':
            self.stack.append((self.B, node))
            self.stack.append(('ID', node))
            self.stack.append(self.code_gen.pid)
        else:
            self.error_handler('Expression', self.Expression, node)

    def B(self, parent):
        node = Node('B', parent)
        if self.terminal == '=':
            self.stack.append(self.code_gen.assign)
            self.stack.append((self.Expression, node))
            self.stack.append(('=', node))
        elif self.terminal == '[':
            self.stack.append((self.H, node))
            self.stack.append((']', node))
            self.stack.append(self.code_gen.offset)
            self.stack.append((self.Expression, node))
            self.stack.append(('[', node))
        elif self.terminal in self.grammar['First']['Simple-expression-prime'] or self.terminal in \
                self.grammar['Follow']['B']:
            self.stack.append((self.Simple_expression_prime, node))
        else:
            self.error_handler('B', self.B, node)

    def H(self, parent):
        node = Node('H', parent)
        if self.terminal == '=':
            self.stack.append(self.code_gen.assign)
            self.stack.append((self.Expression, node))
            # self.stack.append(self.code_gen.allocate_array)
            self.stack.append(('=', node))
        elif self.terminal in self.grammar['First']['G'] or self.terminal in self.grammar['First'][
            'D'] or self.terminal in self.grammar['First']['C'] or self.terminal in self.grammar['Follow']['H']:
            self.stack.append((self.C, node))
            self.stack.append((self.D, node))
            self.stack.append((self.G, node))
        else:
            self.error_handler('H', self.H, node)

    def Simple_expression_zegond(self, parent):
        node = Node('Simple-expression-zegond', parent)
        if self.terminal in self.grammar['First']['Additive-expression-zegond']:
            self.stack.append((self.C, node))
            self.stack.append((self.Additive_expression_zegond, node))
        else:
            self.error_handler('Simple-expression-zegond', self.Simple_expression_zegond, node)

    def Simple_expression_prime(self, parent):
        node = Node('Simple-expression-prime', parent)
        if self.terminal in self.grammar['First']['Additive-expression-prime'] or self.terminal in \
                self.grammar['First']['C'] or self.terminal in self.grammar['Follow']['Simple-expression-prime']:
            self.stack.append((self.C, node))
            self.stack.append((self.Additive_expression_prime, node))
        else:
            self.error_handler('Simple-expression-prime', self.Simple_expression_prime, node)

    def C(self, parent):
        node = Node('C', parent)
        if self.terminal in self.grammar['First']['Relop']:
            self.stack.append(self.code_gen.op)
            self.stack.append((self.Additive_expression, node))
            self.stack.append((self.Relop, node))
        elif self.terminal in self.grammar['Follow']['C']:
            Node('epsilon', node)
        else:
            self.error_handler('C', self.C, node)

    def Relop(self, parent):
        node = Node('Relop', parent)
        if self.terminal == '<':
            self.stack.append(('<', node))
            self.stack.append(self.code_gen.push_lt)
        elif self.terminal == '==':
            self.stack.append(('==', node))
            self.stack.append(self.code_gen.push_eq)
        else:
            self.error_handler('Relop', self.Relop, node)

    def Additive_expression(self, parent):
        node = Node('Additive-expression', parent)
        if self.terminal in self.grammar['First']['Term']:
            self.stack.append((self.D, node))
            self.stack.append((self.Term, node))
        else:
            self.error_handler('Additive-expression', self.Additive_expression, node)

    def Additive_expression_prime(self, parent):
        node = Node('Additive-expression-prime', parent)
        if self.terminal in self.grammar['First']['Term-prime'] or self.terminal in self.grammar['First'][
            'D'] or self.terminal in self.grammar['Follow']['Additive-expression-prime']:
            self.stack.append((self.D, node))
            self.stack.append((self.Term_prime, node))
        else:
            self.error_handler('Additive-expression-prime', self.Additive_expression_prime, node)

    def Additive_expression_zegond(self, parent):
        node = Node('Additive-expression-zegond', parent)
        if self.terminal in self.grammar['First']['Term-zegond']:
            self.stack.append((self.D, node))
            self.stack.append((self.Term_zegond, node))
        else:
            self.error_handler('Additive-expression-zegond', self.Additive_expression_zegond, node)

    def D(self, parent):
        node = Node('D', parent)
        if self.terminal in self.grammar['First']['Addop']:
            self.stack.append((self.D, node))
            self.stack.append(self.code_gen.op)
            self.stack.append((self.Term, node))
            self.stack.append((self.Addop, node))
        elif self.terminal in self.grammar['Follow']['D']:
            Node('epsilon', node)
        else:
            self.error_handler('D', self.D, node)

    def Addop(self, parent):
        node = Node('Addop', parent)
        if self.terminal == '+':
            self.stack.append(('+', node))
            self.stack.append(self.code_gen.push_add)
        elif self.terminal == '-':
            self.stack.append(('-', node))
            self.stack.append(self.code_gen.push_sub)
        else:
            self.error_handler('Addop', self.Addop, node)

    def Term(self, parent):
        node = Node('Term', parent)
        if self.terminal in self.grammar['First']['Factor']:
            self.stack.append((self.G, node))
            self.stack.append((self.Factor, node))
        else:
            self.error_handler('Term', self.Term, node)

    def Term_prime(self, parent):
        node = Node('Term-prime', parent)
        if self.terminal in self.grammar['First']['Factor-prime'] or self.terminal in self.grammar['First'][
            'G'] or self.terminal in self.grammar['Follow']['Term-prime']:
            self.stack.append((self.G, node))
            self.stack.append((self.Factor_prime, node))
        else:
            self.error_handler('Term-prime', self.Term_prime, node)

    def Term_zegond(self, parent):
        node = Node('Term-zegond', parent)
        if self.terminal in self.grammar['First']['Factor-zegond']:
            self.stack.append((self.G, node))
            self.stack.append((self.Factor_zegond, node))
        else:
            self.error_handler('Term-zegond', self.Term_zegond, node)

    def G(self, parent):
        node = Node('G', parent)
        if self.terminal == '*':
            self.stack.append((self.G, node))
            self.stack.append(self.code_gen.mult)
            self.stack.append((self.Factor, node))
            self.stack.append(('*', node))
        elif self.terminal in self.grammar['Follow']['G']:
            Node('epsilon', node)
        else:
            self.error_handler('G', self.G, node)

    def Factor(self, parent):
        node = Node('Factor', parent)
        if self.terminal == '(':
            self.stack.append((')', node))
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
        elif self.terminal == 'ID':
            self.stack.append((self.Var_call_prime, node))
            self.stack.append(('ID', node))
            self.stack.append(self.code_gen.pid)
        elif self.terminal == 'NUM':
            self.stack.append(('NUM', node))
            self.stack.append(self.code_gen.pnum)
        else:
            self.error_handler('Factor', self.Factor, node)

    def Var_call_prime(self, parent):
        node = Node('Var-call-prime', parent)
        if self.terminal == '(':
            self.stack.append((')', node))
            self.stack.append(self.code_gen.call_after_args)
            self.stack.append((self.Args, node))
            self.stack.append(self.code_gen.init_call)
            self.stack.append(('(', node))
        elif self.terminal in self.grammar['First']['Var-prime'] or self.terminal in self.grammar['Follow'][
            'Var-call-prime']:
            self.stack.append((self.Var_prime, node))
        else:
            self.error_handler('Var-call-prime', self.Var_call_prime, node)

    def Var_prime(self, parent):
        node = Node('Var-prime', parent)
        if self.terminal == '[':
            self.stack.append((']', node))
            self.stack.append(self.code_gen.offset)
            self.stack.append((self.Expression, node))
            self.stack.append(('[', node))
        elif self.terminal in self.grammar['Follow']['Var-prime']:
            Node('epsilon', node)
        else:
            self.error_handler('Var-prime', self.Var_prime, node)

    def Factor_prime(self, parent):
        node = Node('Factor-prime', parent)
        if self.terminal == '(':
            self.stack.append((')', node))
            self.stack.append(self.code_gen.call_after_args)
            self.stack.append((self.Args, node))
            self.stack.append(self.code_gen.init_call)
            self.stack.append(('(', node))
        elif self.terminal in self.grammar['Follow']['Factor-prime']:
            Node('epsilon', node)
        else:
            self.error_handler('Factor-prime', self.Factor_prime, node)

    def Factor_zegond(self, parent):
        node = Node('Factor-zegond', parent)
        if self.terminal == '(':
            self.stack.append((')', node))
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
        elif self.terminal == 'NUM':
            self.stack.append(('NUM', node))
            self.stack.append(self.code_gen.pnum)
        else:
            self.error_handler('Factor-zegond', self.Factor_zegond, node)

    def Args(self, parent):
        node = Node('Args', parent)
        if self.terminal in self.grammar['First']['Arg-list']:
            self.stack.append((self.Arg_list, node))
        elif self.terminal in self.grammar['Follow']['Args']:
            Node('epsilon', node)
        else:
            self.error_handler('Args', self.Args, node)

    def Arg_list(self, parent):
        node = Node('Arg-list', parent)
        if self.terminal in self.grammar['First']['Expression']:
            self.stack.append((self.Arg_list_prime, node))
            self.stack.append(self.code_gen.add_arg)
            self.stack.append((self.Expression, node))
        else:
            self.error_handler('Arg-list', self.Arg_list, node)

    def Arg_list_prime(self, parent):
        node = Node('Arg-list-prime', parent)
        if self.terminal == ',':
            self.stack.append((self.Arg_list_prime, node))
            self.stack.append(self.code_gen.add_arg)
            self.stack.append((self.Expression, node))
            self.stack.append((',', node))
        elif self.terminal in self.grammar['Follow']['Arg-list-prime']:
            Node('epsilon', node)
        else:
            self.error_handler('Arg-list-prime', self.Arg_list_prime, node)
