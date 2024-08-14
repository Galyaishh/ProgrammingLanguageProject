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
    INVALID = auto()  # New token type for invalid characters


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

        # Integer
        if current_char.isdigit() or current_char == '-':
            integer_pattern = r'-?\d+'
            match = re.match(integer_pattern, self.text[self.pos:])
            if match:
                value = int(match.group())
                self.pos += len(match.group())
                return Token(TokenType.INTEGER, value)

        # Boolean
        boolean_pattern = r'True|False'
        match = re.match(boolean_pattern, self.text[self.pos:])
        if match:
            value = match.group() == 'True'
            self.pos += len(match.group())
            return Token(TokenType.BOOLEAN, value)

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

        # If we've reached this point, the character is invalid
        self.pos += 1
        return Token(TokenType.INVALID, current_char)


# Test the lexer
def test_lexer():
    test_cases = [
        "42 + 10",
        "15 - 5",
        "3 * 7",
        "20 / 4",
        "17 % 5",
        "True && False",
        "True || False",
        "!True",
        "10 + 5 * 2 - 8 / 4 % 3",
        "True && !False || True",
        "5 == 5",
        "10 != 5",
        "7 > 3",
        "2 < 8",
        "6 >= 6",
        "4 <= 5",
        "1 + 2 == 3 && 4 * 5 > 15",
        "Hello World",  # This should produce INVALID tokens
        "3 $ 4"  # This should produce an INVALID token for $
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
            print(token)  # Print EOF token
        except LexerError as e:
            print(f"Lexer Error: {str(e)}")


if __name__ == "__main__":
    test_lexer()
