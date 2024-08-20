import sys

from interpreter import Interpreter
from lexer import Lexer
from parserR import Parser, ParserError


def main():
    debug_mode = False
    interpreter = Interpreter()

    if len(sys.argv) in [2, 3]:
        filename = sys.argv[1]
        if len(sys.argv) == 3 and sys.argv[2] == '-d':
            debug_mode = True

        if filename.endswith(".lambda"):
            run_file(filename, debug_mode)
        else:
            print("File must have a .lambda extension")
    else:
        run_interactive_mode(interpreter, debug_mode)


def run_interactive_mode(interpreter, debug_mode):
    while True:
        try:
            prompt = 'debug>> ' if debug_mode else 'foo>> '
            text = input(prompt)
            if text.lower() in ['exit', 'quit']:
                break
            if text.lower() == 'debug':
                debug_mode = not debug_mode
                print(f"Debug mode {'enabled' if debug_mode else 'disabled'}")
                continue
        except EOFError:
            break

        if not text:
            continue

        execute_single_statement(text, interpreter, debug_mode)


def execute_single_statement(text, interpreter, debug_mode):
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()
        if debug_mode:
            print(tree)
        result = interpreter.interpret(tree)
        if result:
            print(result)
        if debug_mode:
            print("Interpreter current env:\n", interpreter.env)
    except ParserError as e:
        print(f"Parser Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def run_program(program_text, debug_mode):
    interpreter = Interpreter()
    lexer = Lexer(program_text)
    parser = Parser(lexer)
    try:
        ast = parser.parse()
        if debug_mode:
            print(ast)
        for statement in ast:
            result = interpreter.interpret(statement)
            if result:
                print(result)
    except Exception as e:
        print(f"Error executing program: {e}")


def run_file(filename, debug_mode):
    try:
        with open(filename, 'r') as file:
            program_text = file.read()
        run_program(program_text, debug_mode)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error reading or executing file: {e}")


if __name__ == '__main__':
    main()
