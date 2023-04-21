from anytree import Node, RenderTree
from scanner import *


class Parser:
    def __init__(self, input_file):
        self.stack = []
        self.scanner = Scanner(input_file)
        self.grammar = {'First': dict(), 'Follow': dict()}

    def next_token(self):
        self.current_token = self.scanner.get_next_token()
        if self.current_token[0] == 'NUM' or self.current_token[0] == 'ID':  # get terminal form
            self.terminal = self.current_token[0]
        else:
            self.terminal = self.current_token[1]

    def generate_tree(self):
        self.Program()
        while len(self.stack):
            edge, parent = self.stack.pop()
            if callable(edge):
                self.edge(parent)
            else:
                if edge == self.terminal:
                    Node(f"({self.current_token[0]}, {self.current_token[1]})", parent)
                    self.next_token()
                # else error

    def Program(self):
        self.root = Node("Program")
        if self.terminal in self.grammar['First']['Declaration-list']:
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
            self.stack.append((self.Type_specifier, node))
        else:
            self.error_handler('Declaration-initial', self.Declaration_initial, node)

    def Declaration_prime(self, parent):
        node = Node('Declaration-prime', parent)
        if self.terminal in self.grammar['First']['Fun-declaration-prime']:
            self.stack.append((self.Fun_declaration_prime, node))
        elif self.terminal in self.grammar['First']['Var-declaration-prime']:
            self.stack.append((self.Var_declaration_prime, node))
        else:
            self.error_handler('Declaration-prime', self.Declaration_prime, node)

    def Var_declaration_prime(self, parent):
        node = Node('Var-declaration-primee', parent)
        if self.terminal == ';':
            self.stack.append((';', node))
        elif self.terminal == '[':
            self.stack.append((';', node))
            self.stack.append((']', node))
            self.stack.append(('NUM', node))
            self.stack.append(('[', node))
        else:
            self.error_handler('Var-declaration-prime', self.Var_declaration_prime, node)

    def Fun_declaration_prime(self, parent):
        node = Node('Fun-declaration-prime', parent)
        if self.terminal == '(':
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
        elif self.terminal in self.grammar['Follow']['Param-prime']:
            Node('epsilon', node)
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
        if self.terminal in self.grammar['First']['Expression-stmt']:
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
            self.stack.append((';', node))
            self.stack.append((self.Expression, node))
        elif self.terminal == 'break':
            self.stack.append((';', node))
            self.stack.append(('break', node))
        elif self.terminal == ';':
            self.stack.append((';', node))
        else:
            self.error_handler('Expression-stmt', self.Expression_stmt, node)

    def Selection_stmt(self, parent):
        node = Node('Selection-stmt', parent)
        if self.terminal == 'if':
            self.stack.append((self.Statement, node))
            self.stack.append(('else', node))
            self.stack.append((self.Statement, node))
            self.stack.append((')', node))
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
            self.stack.append(('if', node))
        else:
            self.error_handler('Selection-stmt', self.Selection_stmt, node)

    def Iteration_stmt(self, parent):
        node = Node('Iteration-stmt', parent)
        if self.terminal == 'repeat':
            self.stack.append((')', node))
            self.stack.append((self.Expression, node))
            self.stack.append(('(', node))
            self.stack.append(('untill', node))
            self.stack.append((self.Statement, node))
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
            self.stack.append((self.Expression, node))
        elif self.terminal == ';':
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
        else:
            self.error_handler('Expression', self.Expression, node)

    def B(self, parent):
        node = Node('B', parent)
        if self.terminal in self.grammar['First']['Expression']:
            self.stack.append((self.Expression, node))
        elif self.terminal == '[':
            self.stack.append((self.H, node))
            self.stack.append((']', node))
            self.stack.append((self.Expression, node))
            self.stack.append(('[', node))
        elif self.terminal in self.grammar['First']['Simple-expression-prime']:
            self.stack.append((self.Simple_expression_prime, node))
        else:
            self.error_handler('B', self.B, node)

    def H(self, parent):
        node = Node('H', parent)
        if self.terminal in self.grammar['First']['Expression']:
            self.stack.append((self.Expression, node))
        elif self.terminal in self.grammar['First']['G']:
            self.stack.append((self.G, node))
            self.stack.append((self.D, node))
            self.stack.append((self.C, node))
        else:
            self.error_handler('H', self.H, node)

    def Simple_expression_zegond(self, parent):
        node = Node('Simple_expression_zegond', parent)
        if self.terminal in self.grammar['First']['Additive_expression_zegond']:
            self.stack.append((self.Additive_expression_zegond, node))
            self.stack.append((self.C, node))
        else:
            self.error_handler('Simple_expression_zegond', self.Simple_expression_zegond, node)

    def Simple_expression_prime(self, parent):
        node = Node('Simple_expression_prime', parent)
        if self.terminal in self.grammar['First']['Additive_expression_prime']:
            self.stack.append((self.Additive_expression_prime, node))
            self.stack.append((self.C, node))
        else:
            self.error_handler('Simple_expression_prime', self.Simple_expression_prime, node)

    def C(self, parent):
        node = Node('C', parent)
        if self.terminal in self.grammar['First']['Relop']:
            self.stack.append((self.Relop, node))
            self.stack.append((self.Additive_expression, node))
        elif self.terminal in self.grammar['Follow']['C']:
            Node('epsilon', node)
        else:
            self.error_handler('C', self.C, node)

    def Relop(self, parent):
        node = Node('Relop', parent)
        if self.terminal == '<':
            self.stack.append(('<', node))
        elif self.terminal == '==':
            self.stack.append(('==', node))
        else:
            self.error_handler('Relop', self.Relop, node)

    def Additive_expression(self, parent):
        node = Node('Additive_expression', parent)
        if self.terminal in self.grammar['First']['Term']:
            self.stack.append((self.Term, node))
            self.stack.append((self.D, node))
        else:
            self.error_handler('Additive_expression', self.Additive_expression, node)

    def Additive_expression_prime(self, parent):
        node = Node('Additive_expression_prime', parent)
        if self.terminal in self.grammar['First']['Term_prime']:
            self.stack.append((self.Term_prime, node))
            self.stack.append((self.D, node))
        else:
            self.error_handler('Additive_expression_prime', self.Additive_expression_prime, node)

    def Additive_expression_zegond(self, parent):
        node = Node('Additive_expression_zegond', parent)
        if self.terminal in self.grammar['First']['Term_zegond']:
            self.stack.append((self.Term_zegond, node))
            self.stack.append((self.D, node))
        else:
            self.error_handler('Additive_expression_zegond', self.Additive_expression_zegond, node)

    def D(self, parent):
        node = Node('D', parent)
        if self.terminal in self.grammar['First']['Addop']:
            self.stack.append((self.Addop, node))
            self.stack.append((self.Term, node))
            self.stack.append((self.D, node))
        elif self.terminal in self.grammar['Follow']['D']:
            Node('epsilon', node)
        else:
            self.error_handler('D', self.D, node)

    def Addop(self, parent):
        node = Node('Addop', parent)
        if self.terminal == '+':
            self.stack.append(('+', node))
        elif self.terminal == '-':
            self.stack.append(('-', node))
        else:
            self.error_handler('Addop', self.Addop, node)

    def Term(self, parent):
        node = Node('Term', parent)
        if self.terminal in self.grammar['First']['Factor']:
            self.stack.append((self.Factor, node))
            self.stack.append((self.G, node))
        else:
            self.error_handler('Term', self.Term, node)

    def Term_prime(self, parent):
        node = Node('Term_prime', parent)
        if self.terminal in self.grammar['First']['Factor_prime']:
            self.stack.append((self.Factor_prime, node))
            self.stack.append((self.G, node))
        else:
            self.error_handler('Term_prime', self.Term_prime, node)

    def Term_zegond(self, parent):
        node = Node('Term_zegond', parent)
        if self.terminal in self.grammar['First']['Factor_zegond']:
            self.stack.append((self.Factor_zegond, node))
            self.stack.append((self.G, node))
        else:
            self.error_handler('Term_zegond', self.Term_zegond, node)

    def G(self, parent):
        node = Node('G', parent)
        if self.terminal == '*':
            self.stack.append(('*', node))
            self.stack.append((self.Factor, node))
            self.stack.append((self.G, node))
        elif self.terminal in self.grammar['Follow']['G']:
            Node('epsilon', node)
        else:
            self.error_handler('G', self.G, node)

    def Factor(self, parent):
        node = Node('Factor', parent)
        if self.terminal == '(':
            self.stack.append(('(', node))
            self.stack.append((self.Expression, node))
            self.stack.append((')', node))
        elif self.terminal == 'ID':
            self.stack.append(('ID', node))
            self.stack.append((self.Var_call_prime, node))
        elif self.terminal == 'NUM':
            self.stack.append(('NUM', node))
        else:
            self.error_handler('Factor', self.Factor, node)

    def Var_call_prime(self, parent):
        node = Node('Var_call_prime', parent)
        if self.terminal == '(':
            self.stack.append(('(', node))
            self.stack.append((self.Args, node))
            self.stack.append((')', node))
        elif self.terminal in self.grammar['First']['Var_prime']:
            self.stack.append((self.Var_prime, node))
        else:
            self.error_handler('Var_call_prime', self.Var_call_prime, node)

    def Var_prime(self, parent):
        node = Node('Var_prime', parent)
        if self.terminal == '[':
            self.stack.append(('[', node))
            self.stack.append((self.Expression, node))
            self.stack.append((']', node))
        elif self.terminal in self.grammar['Follow']['Var_prime']:
            Node('epsilon', node)
        else:
            self.error_handler('Var_prime', self.Var_prime, node)

    def Factor_prime(self, parent):
        node = Node('Factor_prime', parent)
        if self.terminal == '(':
            self.stack.append(('(', node))
            self.stack.append((self.Args, node))
            self.stack.append((')', node))
        elif self.terminal in self.grammar['Follow']['Factor_prime']:
            Node('epsilon', node)
        else:
            self.error_handler('Factor_prime', self.Factor_prime, node)

    def Factor_zegond(self, parent):
        node = Node('Factor_zegond', parent)
        if self.terminal == '(':
            self.stack.append(('(', node))
            self.stack.append((self.Expression, node))
            self.stack.append((')', node))
        elif self.terminal == 'NUM':
            self.stack.append(('NUM', node))
        else:
            self.error_handler('Factor_zegond', self.Factor_zegond, node)

    def Args(self, parent):
        node = Node('Args', parent)
        if self.terminal in self.grammar['First']['Arg_list']:
            self.stack.append((self.Arg_list, node))
        elif self.terminal in self.grammar['Follow']['Args']:
            Node('epsilon', node)
        else:
            self.error_handler('Args', self.Args, node)

    def Arg_list(self, parent):
        node = Node('Arg_list', parent)
        if self.terminal in self.grammar['First']['Expression']:
            self.stack.append((self.Expression, node))
            self.stack.append((self.Arg_list_prime, node))
        else:
            self.error_handler('Arg_list', self.Arg_list, node)

    def Arg_list_prime(self, parent):
        node = Node('Arg_list_prime', parent)
        if self.terminal == ',':
            self.stack.append((',', node))
            self.stack.append((self.Expression, node))
            self.stack.append((self.Arg_list_prime, node))
        elif self.terminal in self.grammar['Follow']['Arg_list_prime']:
            Node('epsilon', node)
        else:
            self.error_handler('Arg_list_prime', self.Arg_list_prime, node)
