from lexer import TokenType, Lexer
from parserR import Parser


class NodeVisitor:
    def visit(self, node):
        return node.accept(self)


class Interpreter(NodeVisitor):
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

    def interpret(self, tree):
        return self.visit(tree)


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


if __name__ == "__main__":
    test_interpreter()
