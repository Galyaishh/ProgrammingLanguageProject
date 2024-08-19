from interpreter import Interpreter
from lexer import Lexer
from parserR import Parser, ParserError


def main():
    interpreter = Interpreter()

    while True:
        try:
            text = input('foo>> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        try:
            tree = parser.parse()
            print(tree)
            result = interpreter.interpret(tree)
            print(result)
            print(interpreter.env)
        except ParserError as e:
            print(f"Parser Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
