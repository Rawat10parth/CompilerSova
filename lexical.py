
class Lexical_Analyser:
        def __init__(self, file_name, text):
                self.file_name = file_name
                self.text = text
                self.pos = Position(-1, 0, -1, file_name, text)
                self.current_char = None
                self.next()

        def next(self):
                self.pos.next(self.current_char)
                self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

        @property
        def token_generator(self):
                tokens = []

                while self.current_char is not None:
                        # Ignoring the characters such as spaces and tabs
                        if self.current_char in ' \t':
                                self.next()
                        # Ignoring the characters which starts with #
                        elif self.current_char == '#':
                                self.comments()
                        # Creating Function for Digits
                        elif self.current_char in DIGITS:
                                tokens.append(self.number_generation())
                        # Creating Function for Letters
                        elif self.current_char in LETTERS:
                                tokens.append(self.identifier_generation())
                        # Creating Function for String "which are written in double inverted comma's"
                        elif self.current_char == '"':
                                tokens.append(self.string_generation())
                        # Creating Function for String 'which are written in inverted comma's'
                        elif self.current_char == "'":
                                tokens.append(self.string_generation())
                        # Creating Function for Nextline character
                        elif self.current_char == '\n':
                                tokens.append(Tokens(Tokentype_NEWLINE, pos_start=self.pos))

                        elif self.current_char == '+':
                                tokens.append(self.increment_generation())
                                self.next()

                        elif self.current_char == '-':
                                tokens.append(Tokens(self.decrement_generation()))
                                self.next()

                        elif self.current_char == '*':
                                tokens.append(Tokens(self.Exponent_generation()))
                                self.next()

                        elif self.current_char == '/':
                                tokens.append(Tokens(self.divide_assigment_generation()))
                                self.next()

                        elif self.current_char == '(':
                                tokens.append(Tokens(Tokentype_LPAREN))
                                self.next()

                        elif self.current_char == ')':
                                tokens.append(Tokens(Tokentype_RPAREN))
                                self.next()

                        elif self.current_char == '[':
                                tokens.append(Tokens(Tokentype_LSQUARE))
                                self.next()

                        elif self.current_char == ']':
                                tokens.append(Tokens(Tokentype_RSQUARE))
                                self.next()

                        elif self.current_char == '{':
                                tokens.append(Tokens(Tokentype_LCURLY))
                                self.next()

                        elif self.current_char == '}':
                                tokens.append(Tokens(Tokentype_RCURLY))
                                self.next()

                        elif self.current_char == '^':
                                tokens.append(Tokens(Tokentype_BITWISE_XOR))
                                self.next()

                        elif self.current_char == '!':
                                token, error = self.not_equals_generation()
                                if error: return [], error
                                tokens.append(token)

                        elif self.current_char == '=':
                                tokens.append(self.equals_generation())

                        elif self.current_char == '<':
                                tokens.append(self.less_than_generation())

                        elif self.current_char == '>':
                                tokens.append(self.greater_than_generation())

                        elif self.current_char == ',':
                                tokens.append(Tokens(Tokentype_COMMA, self.current_char))
                                self.next()

                        elif self.current_char == ':':
                                tokens.append(Tokens(Tokentype_COLON, self.current_char))
                                self.next()

                        elif self.current_char == ';':
                                tokens.append(Tokens(Tokentype_SEMICOLON, self.current_char))
                                self.next()

                        elif self.current_char == '&':
                                tokens.append(self.and_log_bit())

                        elif self.current_char == '|':
                                tokens.append(self.or_log_bit())

                        elif self.current_char == '%':
                                tokens.append(Tokens(Tokentype_MODULO))
                                self.next()

                        else:
                                pos_first = self.pos.copy()
                                char = self.current_char
                                self.next()
                                return [], IllegalCharError(pos_first, self.pos, "'"+ char + "'")

                tokens.append(Tokens(Tokentype_EOF))
                return tokens, None

        def comments(self):
                while self.current_char is not None and self.current_char != '\n':
                        self.next()

        def number_generation(self):
                num_str = ''
                dot_count = 0

                while self.current_char is not None and self.current_char in DIGITS + '.':
                        if self.current_char == '.':
                                if dot_count == 1:
                                        break
                                dot_count += 1
                                num_str += '.'
                        else:
                                num_str += self.current_char
                        self.next()

                if dot_count == 0:
                        return Tokens(Tokens(Tokentype_INT), int(num_str))
                else:
                        return Tokens(Tokens(Tokentype_FLOAT), float(num_str))

        def identifier_generation(self):
                identifier_str = ''

                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                        identifier_str += self.current_char
                        self.next()

                if identifier_str.lower() == 'true':
                        return Tokens(Tokentype_BOOLEAN, True)
                elif identifier_str.lower() == 'false':
                        return Tokens(Tokentype_BOOLEAN, 'False')
                elif identifier_str in KEYWORDS:
                        token_type = Tokentype_KEYWORD if identifier_str in KEYWORDS else Tokentype_IDENTIFIER
                        return Tokens(token_type, identifier_str)
                else:
                        return Tokens(Tokentype_IDENTIFIER, identifier_str)

        def string_generation(self):
                string = ''
                pos_start = self.pos.copy()
                escape_character = False
                self.next()

                escape_characters = {
                        'n': '\n',
                        't': '\t'
                }

                while self.current_char is not None and (self.current_char != '"' or escape_character):
                        if escape_character:
                                string += escape_characters.get(self.current_char, self.current_char)
                        else:
                                if self.current_char == '\\':
                                        escape_character = True
                                else:
                                        string += self.current_char
                        self.next()
                        escape_character = False

                self.next()
                return Tokens(Tokentype_STRING, string, pos_start, self.pos)

        def not_equals_generation(self):
                start_pos = self.pos.copy()

                self.next()

                if self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_NOTEQUALS), None
                else:
                        return None, Error.ExpectedCharError(start_pos, self.pos, 'Expected "=" after "!"')


        def equals_generation(self):
                self.next()
                if self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_EE)
                else:
                        return Tokens(Tokentype_EQUALS)

        def less_than_generation(self):
                self.next()
                if self.current_char == '<':
                        self.next()
                        return Tokens(Tokentype_LEFT_SHIFT)
                elif self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_LE)
                else:
                        return Tokens(Tokentype_LESS)

        def greater_than_generation(self):
                self.next()
                if self.current_char == '>':
                        self.next()
                        return Tokens(Tokentype_RIGHT_SHIFT)
                elif self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_GE)
                else:
                        return Tokens(Tokentype_GREATER)

        def and_log_bit(self):
                self.next()
                if self.current_char == '&':
                        self.next()
                        return Tokens(Tokentype_LOGICAL_AND)
                else:
                        return Tokens(Tokentype_BITWISE_AND)

        def or_log_bit(self):
                self.next()
                if self.current_char == '|':
                        self.next()
                        return Tokens(Tokentype_LOGICAL_OR)
                else:
                        return Tokens(Tokentype_BITWISE_OR)

        def increment_generation(self):
                self.next()
                if self.current_char == '+':
                        self.next()
                        return Tokens(Tokentype_INC)
                elif self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_ADD_ASSIGN)
                else:
                        return Tokens(Tokentype_PLUS)

        def decrement_generation(self):
                self.next()
                if self.current_char == '-':
                        self.next()
                        return Tokens(Tokentype_DRC)
                elif self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_MIN_ASSIGN)
                else:
                        return Tokens(Tokentype_MINUS)

        def Exponent_generation(self):
                self.next()
                if self.current_char == '*':
                        self.next()
                        return Tokens(Tokentype_EXPO)
                elif self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_MUL_ASSIGN)
                else:
                        return Tokens(Tokentype_MUL)

        def divide_assigment_generation(self):
                self.next()
                if self.current_char == '=':
                        self.next()
                        return Tokens(Tokentype_DIV_ASSIGN)
                else:
                        return Tokens(Tokentype_DIV)


class Tokens:

    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
            if self.value:
                    return f'{self.type}: {self.value}'
            return f'{self.type}'


# POSITION
class Position:
        def __init__(self, index, line_number, column_number, file_name, file_text):
                self.index = index
                self.line_number = line_number
                self.column_number = column_number
                self.file_name = file_name
                self.file_text = file_text

        def next(self, current_char):
                self.index += 1
                self.column_number += 1

                if current_char == '\n':
                        self.line_number += 1
                        self.column_number += 0

                return self

        def copy(self):
                return Position(self.index, self.line_number, self.column_number, self.file_name, self.file_text)


# ERRORS
class Error:
        def __init__(self, pos_first, pos_end, error_name, details):
                self.pos_first = pos_first
                self.pos_end = pos_end
                self.error_name = error_name
                self.details = details


        def as_string(self):
                result = f'{self.error_name}: {self.details}'
                result += f'File {self.pos_first.file_name}, line {self.pos_first.line_number + 1}'
                return result

        @classmethod
        def ExpectedCharError(cls, start_pos, pos, details):
                return cls(start_pos, pos, 'Expected Character', details)


class IllegalCharError(Error):
        def __init__(self, pos_first, pos_end, details):
                super().__init__(pos_first, pos_end, 'Illegal Character', details)


# To initiate the lexical analysis process
def run(file_name, text):
        lexer = Lexical_Analyser(file_name, text)
        tokens, error = lexer.token_generator

        return tokens, error

# TOKENS

# Operators
Tokentype_INT = 'INTEGER'
Tokentype_FLOAT = 'FLOAT'
Tokentype_STRING = 'STRING'
Tokentype_PLUS = 'ADDITION'
Tokentype_MINUS = 'SUBTRACTION'
Tokentype_MUL = 'MULTIPLY'
Tokentype_DIV = 'DIVIDE'
Tokentype_EXPO = 'EXPONENT'
Tokentype_IDENTIFIER = 'IDENTIFIER'
Tokentype_KEYWORD = 'KEYWORD'
Tokentype_EQUALS = 'ASSIGMENT'
Tokentype_NOTEQUALS = 'NOTEQUALS'
Tokentype_GREATER = 'GREATER'
Tokentype_GE = 'GREATER_THAN_EQUAL'
Tokentype_LESS = 'LESS'
Tokentype_LE = 'LESS_THAN_EQUAL'

# Scope and Blocks
Tokentype_LPAREN = 'LPAREN'
Tokentype_RPAREN = 'RPAREN'
Tokentype_LSQUARE = 'LSQUARE'
Tokentype_RSQUARE = 'RSQUARE'
Tokentype_LCURLY = 'LCURLY'
Tokentype_RCURLY = 'RCURLY'

Tokentype_NEWLINE = 'NEWLINE'

Tokentype_SEMICOLON = 'SEMICOLON'
Tokentype_COMMA = 'COMMA'
Tokentype_COLON = 'COLON'

Tokentype_EOF = 'END_OF_FILE'

# Bitwise Operators
Tokentype_BITWISE_AND = 'BITWISE_AND'
Tokentype_BITWISE_OR = 'BITWISE_OR'
Tokentype_BITWISE_XOR = 'BITWISE_XOR'
Tokentype_MODULO = 'MODULO'
Tokentype_BOOLEAN = 'BOOLEAN'

# Increment and Decrement
Tokentype_INC = 'INCREMENT'
Tokentype_DRC = 'DECREMENT'
Tokentype_EE = 'EQUALS'

# Assignment Operators
Tokentype_ADD_ASSIGN = 'ADD_ASSIGNMENT'
Tokentype_MIN_ASSIGN = 'MINUS_ASSIGNMENT'
Tokentype_MUL_ASSIGN = 'MULTIPLY_ASSIGNMENT'
Tokentype_DIV_ASSIGN = 'DIVIDE_ASSIGNMENT'

# Bitwise Shift Assignment
Tokentype_LEFT_SHIFT = 'LEFT_SHIFT'
Tokentype_RIGHT_SHIFT = 'RIGHT_SHIFT'

# Logical Assignment
Tokentype_LOGICAL_AND = 'LOGICAL_AND'
Tokentype_LOGICAL_OR = 'LOGICAL_OR'

# CONSTANTS
DIGITS = '0123456789'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# KEYWORDS
KEYWORDS = ['VAR', 'AND', 'OR', 'NOT', 'IF', 'ELSE', 'ELIF', 'WHILE', 'FOR', 'FUNCTION', 'RETURN', 'DEF', 'PRINT',
            'var', 'and', 'or', 'not', 'if', 'else', 'elif', 'while', 'for', 'function', 'return', 'def', 'print']