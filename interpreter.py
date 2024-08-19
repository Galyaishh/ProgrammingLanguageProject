from lexer import TokenType, Lexer
from parserR import Parser, LambdaExpression, FunctionDef


class NodeVisitor:
    def visit(self, node):
        return node.accept(self)

class Interpreter(NodeVisitor):

    def __init__(self):
        self.env = {}

    def visit_BinaryOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIVIDE:
            return self.visit(node.left) // self.visit(node.right)  # Integer division
        elif node.op.type == TokenType.MODULO:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == TokenType.AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == TokenType.OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.type == TokenType.EQUAL:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == TokenType.NOT_EQUAL:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == TokenType.GREATER_THAN:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == TokenType.LESS_THAN:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == TokenType.GREATER_THAN_OR_EQUAL:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == TokenType.LESS_THAN_OR_EQUAL:
            return self.visit(node.left) <= self.visit(node.right)
        else:
            raise Exception(f'Invalid operator {node.op}')

    def visit_UnaryOp(self, node):
        if node.op.type == TokenType.NOT:
            return not self.visit(node.expr)
        else:
            raise Exception(f'Invalid operator {node.op}')

    def visit_Number(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_Variable(self, node):
        var_name = str(node.name)
        if var_name not in self.env:
            raise Exception(f"Variable '{var_name}' is not defined")

        return self.env[var_name]

    def visit_FunctionDef(self, node):
        self.env[node.name] = node
        return None  # Function definitions don't return a value

    def visit_FunctionCall(self, node):
        func = self.env.get(node.name)
        if not func:
            raise Exception(f"Function '{node.name}' is not defined")

        if not isinstance(func, FunctionDef):
            raise Exception(f"'{node.name}' is not a function")

        if len(node.arguments) != len(func.arguments):
            raise Exception(
                f"Function '{node.name}' expects {len(func.arguments)} arguments, but got {len(node.arguments)}")

        # Create a new environment for the function call
        local_env = self.env.copy()
        for param, arg in zip(func.arguments, node.arguments):
            local_env[param] = self.visit(arg)

        # Save the current environment and set the new one
        old_env = self.env
        self.env = local_env

        try:
            # Execute the function body
            result = self.visit(func.body)
        finally:
            # Restore the old environment
            self.env = old_env

        return result

    def interpret(self, tree):
        results = []
        if isinstance(tree, list):
            for node in tree:
                result = self.visit(node)
                if result is not None:
                    results.append(result)
        else:
            results.append(self.visit(tree))
        return results[0]


# Test the interpreter
def test_interpreter():
    test_cases = [
        "42--6",
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
        print(f"\nInterpreting: {case}")
        lexer = Lexer(case)
        parser = Parser(lexer)
        try:
            tree = parser.parse()
            interpreter = Interpreter()
            result = interpreter.interpret(tree)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Interpretation failed: {str(e)}")


def test_interpreter2():
    code = """
    Defun { add, (x, y) }  x + y

    add(5, 3)
    """
    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()

    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    print(result)


if __name__ == "__main__":
    test_interpreter2()
