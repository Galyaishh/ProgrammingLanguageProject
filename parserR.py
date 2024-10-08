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

    def __repr__(self):
        return self.__str__()


class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.op} {self.right})'


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'({self.op}{self.expr})'


class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class FunctionDef(ASTNode):
    def __init__(self, name, arguments, body):
        self.name = name
        self.arguments = arguments
        self.body = body

    def __repr__(self):
        return f"FunctionDef(name={self.name}, arguments={self.arguments}, body={self.body})"


class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall(name={self.name}, arguments={self.arguments})"


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class LambdaExpression(ASTNode):
    def __init__(self, params, args, body):
        self.params = params
        self.args = args
        self.body = body

    def __repr__(self):
        return f"(Lambd {self.params} . {self.body} , {self.args})"

class IfElse(ASTNode):
    def __init__(self, condition, if_branch, else_branch=None):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch

    def __repr__(self):
        if self.else_branch:
            return f"If({self.condition}) {{ {self.if_branch} }} Else {{ {self.else_branch} }}"
        return f"If({self.condition}) {{ {self.if_branch} }}"



class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, details=None):
        red_det = f"Syntax error: {details}, at {self.lexer.pos} position."
        if details:
            raise Exception(red_det)
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == TokenType.INVALID:
            self.error(f"Invalid token: {self.current_token.value}")
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            if self.current_token.type == TokenType.INVALID:
                self.error(f"Invalid token: {self.current_token.value}")
        else:
            self.error(f"Expected {token_type}, found {self.current_token.type}")

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
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.eat(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.LPAREN:
                return self.function_call(name)
            else:
                return Variable(name)
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
        if self.current_token.type == TokenType.DEFUN:
            return self.function_definition()
        elif self.current_token.type == TokenType.LAMBD:
            return self.lambda_expression()
        return self.boolean_expr()  ## returns a node!!

    def function_call(self, name):
        self.eat(TokenType.LPAREN)
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.expr())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                arguments.append(self.expr())
        self.eat(TokenType.RPAREN)
        return FunctionCall(name, arguments)

    def if_else_statement(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.boolean_expr()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        if_branch = self.expr()  # Or parse a block of statements
        self.eat(TokenType.RBRACE)

        else_branch = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            else_branch = self.expr()  # Or parse a block of statements
            self.eat(TokenType.RBRACE)

        return IfElse(condition, if_branch, else_branch)

    def function_definition(self):
        self.eat(TokenType.DEFUN)
        self.eat(TokenType.LBRACE)

        # Parse function name
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.COMMA)

        # Parse function arguments
        self.eat(TokenType.LPAREN)
        arguments = self.argument_list()
        self.eat(TokenType.RPAREN)

        self.eat(TokenType.RBRACE)

        # Parse function body
        body = self.expr()

        return FunctionDef(name, arguments, body)

    def argument_list(self):
        args = []
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        return args

    def lambda_expression(self):
        self.eat(TokenType.LAMBD)
        params = []

        # Parse parameters
        params.append(self.current_token.value)
        self.eat(TokenType.IDENTIFIER)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.DOT)

        # Parse body
        body = self.expr()

        # Parse arguments
        self.eat(TokenType.LPAREN)
        args = []
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.expr())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.expr())
        self.eat(TokenType.RPAREN)

        return LambdaExpression(params, args, body)

    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.expr())
            if self.current_token.type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
        return statements

    def expr(self):
        if self.current_token.type == TokenType.DEFUN:
            return self.function_definition()
        elif self.current_token.type == TokenType.LAMBD:
            return self.lambda_expression()
        elif self.current_token.type == TokenType.IF:
            return self.if_else_statement()
        return self.boolean_expr()

    def parse(self):
        program = self.parse_program()
        if self.current_token.type != TokenType.EOF:
            self.error(f"Syntax error: got {self.current_token.type} : '{self.current_token.value}'")
        return program


# Test the parser
def test_parser():
    test_cases = [
        "if (x == 5){x + 10} else {5 / 20}",
        "Defun { add, (x, y) } x + y",
        "add(5, 3)",
        "42 - 6",
        "Lambd x.(x+5)(6)",
        "Lambd x,y.(x*y + 5)(3, 4)",
        "Lambd z.(z * z)(10)",
    ]

    for case in test_cases:
        print(f"\nParsing: {case}")
        lexer = Lexer(case)
        parser = Parser(lexer)
        try:
            ast = parser.parse()
            print(ast)
            print("Parsing successful")
            # Here you could add a function to print the AST structure
        except Exception as e:
            print(f"{str(e)}")


if __name__ == "__main__":
    test_parser()
