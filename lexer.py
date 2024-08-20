import re
from enum import Enum, auto


class TokenType(Enum):
    INTEGER = auto()
    BOOLEAN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    LPAREN = auto()
    RPAREN = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN_OR_EQUAL = auto()
    EOF = auto()
    INVALID = auto()
    DEFUN = auto()
    LAMBD = auto()
    IDENTIFIER = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()
    VARIABLE = auto()
    DOT = auto()
    IF = auto()
    ELSE = auto()
    NEWLINE = auto()


class Token:
    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type.name}, {self.value})'


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        return LexerError(f'Invalid character: {self.text[self.pos]}')

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token(TokenType.EOF, None)

        current_char = self.text[self.pos]

        # Skip whitespace
        if current_char.isspace():
            self.pos += 1
            return self.get_next_token()

        if current_char == '#':
            while current_char != '\n' and self.pos < len(self.text):
                self.pos += 1
                current_char = self.text[self.pos]
            self.pos += 1  # Skip the newline character
            return self.get_next_token()

        # Integer
        if current_char.isdigit() or (current_char == '-' and (self.pos == 0 or self.text[self.pos - 1] in '+-*/( ')):
            integer_pattern = r'-?\d+'
            match = re.match(integer_pattern, self.text[self.pos:])
            if match:
                value = int(match.group())
                self.pos += len(match.group())
                return Token(TokenType.INTEGER, value)

        if self.text[self.pos:].startswith("if"):
            self.pos += len("if")
            return Token(TokenType.IF, "if")

        if self.text[self.pos:].startswith("else"):
            self.pos += len("else")
            return Token(TokenType.ELSE, "else")

        # Boolean
        boolean_pattern = r'True|False'
        match = re.match(boolean_pattern, self.text[self.pos:])
        if match:
            value = match.group() == 'True'
            self.pos += len(match.group())
            return Token(TokenType.BOOLEAN, value)

        # Func
        if self.text[self.pos:].startswith("Defun"):
            self.pos += len("Defun")
            return Token(TokenType.DEFUN, "Defun")

        if self.text[self.pos:].startswith("Lambd"):
            self.pos += len("Lambd")
            return Token(TokenType.LAMBD, "Lambd")

        if current_char == '.':
            self.pos += 1
            return Token(TokenType.DOT, '.')
            # Identifiers (e.g., function names)
        if current_char.isalpha():
            identifier_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'
            match = re.match(identifier_pattern, self.text[self.pos:])
            if match:
                value = match.group()
                self.pos += len(match.group())
                return Token(TokenType.IDENTIFIER, value)

                # Arithmetic operations
        if current_char == '+':
            self.pos += 1
            return Token(TokenType.PLUS, '+')
        elif current_char == '-':
            self.pos += 1
            return Token(TokenType.MINUS, '-')
        elif current_char == '*':
            self.pos += 1
            return Token(TokenType.MULTIPLY, '*')
        elif current_char == '/':
            self.pos += 1
            return Token(TokenType.DIVIDE, '/')
        elif current_char == '%':
            self.pos += 1
            return Token(TokenType.MODULO, '%')
        elif current_char == '(':
            self.pos += 1
            return Token(TokenType.LPAREN, '(')
        elif current_char == ')':
            self.pos += 1
            return Token(TokenType.RPAREN, ')')

        # Boolean operations
        if current_char == '&' and self.peek() == '&':
            self.pos += 2
            return Token(TokenType.AND, '&&')
        elif current_char == '|' and self.peek() == '|':
            self.pos += 2
            return Token(TokenType.OR, '||')
        elif current_char == '!':
            if self.peek() == '=':
                self.pos += 2
                return Token(TokenType.NOT_EQUAL, '!=')
            self.pos += 1
            return Token(TokenType.NOT, '!')

        # Comparison operations
        if current_char == '=':
            if self.peek() == '=':
                self.pos += 2
                return Token(TokenType.EQUAL, '==')
        elif current_char == '>':
            if self.peek() == '=':
                self.pos += 2
                return Token(TokenType.GREATER_THAN_OR_EQUAL, '>=')
            self.pos += 1
            return Token(TokenType.GREATER_THAN, '>')
        elif current_char == '<':
            if self.peek() == '=':
                self.pos += 2
                return Token(TokenType.LESS_THAN_OR_EQUAL, '<=')
            self.pos += 1
            return Token(TokenType.LESS_THAN, '<')

            # comma
        if current_char == ',':
            self.pos += 1
            return Token(TokenType.COMMA, ',')

            # Braces
        if current_char == '{':
            self.pos += 1
            return Token(TokenType.LBRACE, '{')

        if current_char == '}':
            self.pos += 1
            return Token(TokenType.RBRACE, '}')

        if current_char == '\n':
            self.pos += 1
            return Token(TokenType.NEWLINE, '\n')
        # If we've reached this point, the character is invalid
        self.pos += 1
        return Token(TokenType.INVALID, current_char)


# Test the lexer
def test_lexer():
    # code = "Defun afiksoco, (n,)}"
    code = """
    Lambd x.(x == 5)
    
    """
    lexer = Lexer(code)

    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        print(token)
        token = lexer.get_next_token()

    test_cases = [
        "if(x == 5) {y = 10} else {y = 20}"
        # "42 + 10 ^",
        # "15 - 5",
        # "3 * 7",
        # "20 / 4",
        # "17 % 5",
        # "True && False",
        # "True || False",
        # "!True",
        # "10 + 5 * 2 - 8 / 4 % 3",
        # "True && !False || True",
        # "5 == 5",
        # "10 != 5",
        # "7 > 3",
        # "2 < 8",
        # "6 >= 6",
        # "4 <= 5",
        # "1 + 2 == 3 && 4 * 5 > 15",
        # "Hello World",  # This should produce INVALID tokens
        # "3 $ 4"  # This should produce an INVALID token for $
    ]

    for case in test_cases:
        print(f"\nLexing: {case}")
        lexer = Lexer(case)
        try:
            token = lexer.get_next_token()
            while token.type != TokenType.EOF:
                print(token)
                if token.type == TokenType.INVALID:
                    print(f"Warning: Invalid token encountered: {token.value}")
                token = lexer.get_next_token()
            print(token)
        except LexerError as e:
            print(f"Lexer Error: {str(e)}")


if __name__ == "__main__":
    test_lexer()
