from lexer import Lexer
from parser import Parser, ParserError
from interpreter import Interpreter


def main():
    while True:
        try:
            text = input('foo>> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter()
        try:
            tree = parser.parse()
            result = interpreter.interpret(tree)
            print(result)
        except ParserError as e:
            print(f"Parser Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
