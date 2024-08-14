from lexer import Lexer, TokenType


class ParserError(Exception):
    pass


class ASTNode:
    def accept(self, visitor):
        method_name = f'visit_{type(self).__name__}'
        visit = getattr(visitor, method_name, self.generic_visit)
        return visit(self)

    def generic_visit(self, visitor):
        raise Exception(f'No visit_{type(self).__name__} method defined')


class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Number(ASTNode):
    def __init__(self, value):
        self.value = value


class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, details=None):
        if details:
            raise Exception(details)
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Number(token.value)
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            if self.current_token.type in (
                    TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
                self.error("Cannot use boolean in arithmetic expression")
            return Boolean(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOp(token, self.factor())
        else:
            self.error(f"Unexpected token {token.type} in factor")

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            elif token.type == TokenType.MODULO:
                self.eat(TokenType.MODULO)
            node = BinaryOp(left=node, op=token, right=self.factor())
        return node

    def arithmetic_expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            right = self.term()
            if isinstance(right, Boolean):
                self.error("Cannot perform arithmetic operations with boolean values")
            node = BinaryOp(left=node, op=token, right=right)
        return node

    def comparison_expr(self):
        node = self.arithmetic_expr()
        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL,
                                          TokenType.GREATER_THAN, TokenType.LESS_THAN,
                                          TokenType.GREATER_THAN_OR_EQUAL, TokenType.LESS_THAN_OR_EQUAL):
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinaryOp(left=node, op=token, right=self.arithmetic_expr())
        return node

    def boolean_expr(self):
        node = self.comparison_expr()
        while self.current_token.type in (TokenType.AND, TokenType.OR):
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinaryOp(left=node, op=token, right=self.comparison_expr())
        return node

    def expr(self):
        return self.boolean_expr()

    def parse(self):
        node = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error("Expected end of input")
        return node


# Parser class
# class Parser:
#     def __init__(self, lexer):
#         self.lexer = lexer
#         self.current_token = self.lexer.get_next_token()
#
#     def error(self, message="Invalid syntax"):
#         raise ParserError(f"{message} at position {self.lexer.pos}")
#
#     def eat(self, token_type):
#         # if self.current_token.type == TokenType.INVALID:
#         #     self.error(f"Invalid token: {self.current_token.value}")
#         if self.current_token.type == token_type:
#             self.current_token = self.lexer.get_next_token()
#             if self.current_token.type == TokenType.INVALID:
#                 self.error(f"Invalid token: {self.current_token.value}")
#         else:
#             self.error(f"Expected {token_type}, found {self.current_token.type}")
#
#     def factor(self):
#         token = self.current_token
#         if token.type == TokenType.INTEGER:
#             self.eat(TokenType.INTEGER)
#             return Number(token.value)
#         elif token.type == TokenType.BOOLEAN:
#             self.eat(TokenType.BOOLEAN)
#             return Boolean(token.value)
#         elif token.type == TokenType.LPAREN:
#             self.eat(TokenType.LPAREN)
#             node = self.expr()
#             self.eat(TokenType.RPAREN)
#             return node
#         elif token.type == TokenType.NOT:
#             self.eat(TokenType.NOT)
#             return UnaryOp(token, self.factor())
#         else:
#             self.error("Invalid factor")
#
#     def term(self):
#         node = self.factor()
#
#         while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
#             token = self.current_token
#             if token.type == TokenType.MULTIPLY:
#                 self.eat(TokenType.MULTIPLY)
#             elif token.type == TokenType.DIVIDE:
#                 self.eat(TokenType.DIVIDE)
#             elif token.type == TokenType.MODULO:
#                 self.eat(TokenType.MODULO)
#
#             node = BinaryOp(left=node, op=token, right=self.factor())
#
#         return node
#
#     def arithmetic_expr(self):
#         node = self.term()
#
#         while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
#             token = self.current_token
#             if token.type == TokenType.PLUS:
#                 self.eat(TokenType.PLUS)
#             elif token.type == TokenType.MINUS:
#                 self.eat(TokenType.MINUS)
#
#             node = BinaryOp(left=node, op=token, right=self.term())
#
#         return node
#
#     def comparison_expr(self):
#         node = self.arithmetic_expr()
#
#         while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL,
#                                           TokenType.GREATER_THAN, TokenType.LESS_THAN,
#                                           TokenType.GREATER_THAN_OR_EQUAL, TokenType.LESS_THAN_OR_EQUAL):
#             token = self.current_token
#             self.eat(self.current_token.type)
#             node = BinaryOp(left=node, op=token, right=self.arithmetic_expr())
#
#         return node
#
#     def boolean_expr(self):
#         node = self.comparison_expr()
#
#         while self.current_token.type in (TokenType.AND, TokenType.OR):
#             token = self.current_token
#             self.eat(self.current_token.type)
#             node = BinaryOp(left=node, op=token, right=self.comparison_expr())
#
#         return node
#
#     def expr(self):
#         return self.boolean_expr()
#
#     def parse(self):
#         node = self.expr()
#         if self.current_token.type != TokenType.EOF:
#             self.error("Expected end of input")
#         return node


# Test the parser
def test_parser():
    test_cases = [
        "True + 42 + 10",
        "15 - 5 * 3",
        "3 * (7 - 2)",
        "20 / 4 % 3",
        "True && False || True",
        "!True && False",
        "5 == 5 && 10 != 5",
        "7 > 3 || 2 < 8",
        "6 >= 6 && 4 <= 5",
        "1 + 2 == 3 && 4 * 5 > 15",
    ]

    for case in test_cases:
        print(f"\nParsing: {case}")
        lexer = Lexer(case)
        parser = Parser(lexer)
        try:
            ast = parser.parse()
            print("Parsing successful")
            # Here you could add a function to print the AST structure
        except Exception as e:
            print(f"Parsing failed: {str(e)}")


if __name__ == "__main__":
    test_parser()
