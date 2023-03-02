from enum import Enum


class State(Enum):
    START = 0
    NUM = 1
    ID = 2
    ASSIGN = 3
    COMMENT1 = 4
    COMMENT2 = 5
    COMMENT3 = 6
    STAR = 7  # for unfinished comment
    END = 8


class TokenName(Enum):

    IF = 0
    ELSE = 1
    INT = 2
    RETURN = 3
    VOID = 4
    REPEAT = 5
    BREAK = 6
    UNTIL = 7

    ADD = 8
    MINUS = 9
    SMALLER = 10
    ASSIGN = 11
    SEMI = 12
    COMMA = 13
    LPAREN = 14
    RPAREN = 15
    LBRACKETS = 16
    RBRACKETS = 17
    LBRACES = 18
    RBRACES = 19
    COLON = 20
    EQUAL = 21
    MULT = 22

    NUM = 23
    ID = 24
    EOF = 25
    INVALID_INPUT = 26
    INVALID_NUM = 27
    UNCLOSED_COMMENT = 28
    UNMATCHED_COMMENT = 29


def get_token_pair(token_name: TokenName, lexeme: str):
    return {
        TokenName.NUM: ('NUM', lexeme),
        TokenName.ID: ('ID', lexeme),
        TokenName.IF: ('KEYWORD', 'if'),
        TokenName.ELSE: ('KEYWORD', 'else'),
        TokenName.VOID: ('KEYWORD', 'void'),
        TokenName.INT: ('KEYWORD', 'int'),
        TokenName.REPEAT: ('KEYWORD', 'repeat'),
        TokenName.BREAK: ('KEYWORD', 'break'),
        TokenName.UNTIL: ('KEYWORD', 'until'),
        TokenName.RETURN: ('KEYWORD', 'return'),
        TokenName.SEMI: ('SYMBOL', ';'),
        TokenName.COLON: ('SYMBOL', ':'),
        TokenName.COMMA: ('SYMBOL', ','),
        TokenName.LBRACKETS: ('SYMBOL', '['),
        TokenName.RBRACKETS: ('SYMBOL', ']'),
        TokenName.LPAREN: ('SYMBOL', '('),
        TokenName.RPAREN: ('SYMBOL', ')'),
        TokenName.LBRACES: ('SYMBOL', '{'),
        TokenName.RBRACES: ('SYMBOL', '}'),
        TokenName.ADD: ('SYMBOL', '+'),
        TokenName.MINUS: ('SYMBOL', '-'),
        TokenName.MULT: ('SYMBOL', '*'),
        TokenName.ASSIGN: ('SYMBOL', '='),
        TokenName.SMALLER: ('SYMBOL', '<'),
        TokenName.EQUAL: ('SYMBOL', '==')
    }[token_name]


def get_token_if_id_is_keyword(lexeme: str):
    return {
        'if': TokenName.IF,
        'else': TokenName.ELSE,
        'void': TokenName.VOID,
        'int': TokenName.INT,
        'repeat': TokenName.REPEAT,
        'break': TokenName.BREAK,
        'until': TokenName.UNTIL,
        'return': TokenName.RETURN,
    }.get(lexeme, TokenName.ID)


def is_char_whitespace(char: str):
    return char in [' ', '\n', '\r', '\t', '\v', '\f']


def is_char_valid(char: str):
    return char.isalnum() or \
        is_char_whitespace(char) or \
        char in ['/', ';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '=='] or \
        char is None


class SymbolTable:
    def __init__(self):
        self.dict = dict()  # {ID/KEYWORD: dict()}

    def initialize_with_keywords(self):
        for key in ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']:
            self.insert(key)

    def exists(self, name):
        return name in self.dict

    def insert(self, name):
        self.dict[name] = dict()


class LexicalErrors:
    def __init__(self):
        self.errors_list = list()
        self.token_name_to_error_string = {
            TokenName.INVALID_INPUT: 'Invalid input',
            TokenName.INVALID_NUM: 'Invalid number',
            TokenName.UNCLOSED_COMMENT: 'Unclosed comment',
            TokenName.UNMATCHED_COMMENT: 'Unmatched comment'
        }

    def add_error(self, lexeme, token_name):
        self.errors_list.append((lexeme, self.token_name_to_error_string[token_name]))


class Scanner:

    def __init__(self, file):
        self.char_idx = 0
        self.lineno = 1
        self.text = file.read()
        self.file_len = len(self.text)
        self.symbol_table = SymbolTable()
        self.symbol_table.initialize_with_keywords()
        self.lexical_errors = LexicalErrors()

    def get_char(self):
        if self.file_len <= self.char_idx:
            return None
        char = self.text[self.char_idx]
        if char == '\n':
            self.lineno += 1
        self.char_idx += 1
        return char

    def pull_back_char_pointer(self):
        self.char_idx -= 1
        if self.text[self.char_idx] == '\n':
            self.lineno -= 1
        return

    def error_occurred(self):
        return self.token_name in [TokenName.INVALID_INPUT,
                                   TokenName.INVALID_NUM,
                                   TokenName.UNCLOSED_COMMENT,
                                   TokenName.UNMATCHED_COMMENT]

    def check_error(self):
        if self.error_occurred():
            lexeme = self.lexeme
            if self.token_name == TokenName.UNCLOSED_COMMENT and len(lexeme) > 7:
                lexeme = lexeme[:7] + '...'
            self.lexical_errors.add_error(lexeme, self.token_name)
            self.state = State.START
            self.lexeme = ''

    def get_next_token(self):

        self.state = State.START
        self.token_name = None
        self.lexeme = ''

        while self.state != State.END:

            self.token_name = None
            self.append_char = True
            char = self.get_char()

            if is_char_valid(char):
                if self.state == State.START:
                    self.handle_start_state(char)
                elif self.state == State.NUM:
                    self.handle_num_state(char)
                elif self.state == State.ID:
                    self.handle_id_state(char)
                elif self.state == State.ASSIGN:
                    self.handle_assign_state(char)
                elif self.state == State.COMMENT1:
                    self.handle_comment1_state(char)
                elif self.state == State.COMMENT2:
                    self.handle_comment2_state(char)
                elif self.state == State.COMMENT3:
                    self.handle_comment3_state(char)
                elif self.state == State.STAR:
                    self.handle_star_state(char)
            else:
                if self.state == State.COMMENT2:
                    self.handle_comment2_state(char)
                elif self.state == State.COMMENT3:
                    self.handle_comment3_state(char)
                else:
                    self.token_name = TokenName.INVALID_INPUT

            if self.error_occurred():
                self.append_char = True

            if self.state == State.COMMENT1 and self.token_name == TokenName.INVALID_INPUT:
                self.append_char = False
                self.lexeme = '/'

            if self.append_char:
                self.lexeme += char

            self.check_error()

            if self.state == State.END and self.token_name == TokenName.ID:
                self.token_name = get_token_if_id_is_keyword(self.lexeme)
                # add to symbol table
                if not self.symbol_table.exists(self.lexeme):
                    self.symbol_table.insert(self.lexeme)

        if not self.token_name == TokenName.EOF:
            return get_token_pair(self.token_name, self.lexeme)
        else:
            return 0

    def handle_assign_state(self, char):
        self.append_char = False
        if char == '=':
            self.token_name = TokenName.EQUAL
        else:
            self.token_name = TokenName.ASSIGN
            if char is not None:
                self.pull_back_char_pointer()
        self.state = State.END

    def handle_comment1_state(self, char):
        self.append_char = True
        if char == '*':
            self.state = State.COMMENT2
        else:
            self.token_name = TokenName.INVALID_INPUT
            if char is not None:
                self.pull_back_char_pointer()

    def handle_comment2_state(self, char):
        self.append_char = True
        if char == '*':
            self.state = State.COMMENT3
        elif char is None:
            self.token_name = TokenName.UNCLOSED_COMMENT

    def handle_comment3_state(self, char):
        self.append_char = True
        if char == '/':
            self.state = State.START
            self.lexeme = ''
            self.append_char = False
        elif char != '*':
            self.state = State.COMMENT2
        elif char is None:
            self.token_name = TokenName.UNCLOSED_COMMENT

    def handle_star_state(self, char):
        if char == '/':
            self.token_name = TokenName.UNMATCHED_COMMENT
        else:
            self.token_name = TokenName.MULT
            self.state = State.END
            if char is not None:
                self.pull_back_char_pointer()

    def handle_num_state(self, char):
        if not char.isnumeric():
            if not char.isalpha():
                self.append_char = False
                self.state = State.END
                self.token_name = TokenName.NUM
                if char is not None:
                    self.pull_back_char_pointer()
            else:
                self.token_name = TokenName.INVALID_NUM

    def handle_id_state(self, char):
        if not char.isalnum():
            self.append_char = False
            self.state = State.END
            self.token_name = TokenName.ID
            if char is not None:
                self.pull_back_char_pointer()

    def handle_start_state(self, char):
        if char.isalpha():
            self.state = State.ID
        elif char.isnumeric():
            self.state = State.NUM
        else:
            self.append_char = False
            if char == '=':
                self.state = State.ASSIGN
            elif char == '/':
                self.state = State.COMMENT1
                self.append_char = True
            elif char == '*':
                self.state = State.STAR
                self.append_char = True
            elif is_char_whitespace(char):
                return
            else:
                self.state = State.END
                if char == '+':
                    self.token_name = TokenName.ADD
                elif char == '-':
                    self.token_name = TokenName.MINUS
                elif char == '[':
                    self.token_name = TokenName.LBRACKETS
                elif char == ']':
                    self.token_name = TokenName.RBRACKETS
                elif char == '(':
                    self.token_name = TokenName.LPAREN
                elif char == ')':
                    self.token_name = TokenName.RPAREN
                elif char == '{':
                    self.token_name = TokenName.LBRACES
                elif char == '}':
                    self.token_name = TokenName.RBRACES
                elif char == ',':
                    self.token_name = TokenName.COMMA
                elif char == ';':
                    self.token_name = TokenName.SEMI
                elif char is None:
                    self.token_name = TokenName.EOF
                else:
                    self.token_name = TokenName.INVALID_INPUT

