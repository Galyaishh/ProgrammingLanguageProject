from interpreter import Interpreter
from lexer import Lexer
from parserR import Parser, ParserError


def main():
    interpreter = Interpreter()
    debug_mode = False

    while True:
        try:
            text = input('foo>> ')
            if text.lower() in ['exit', 'quit']:
                break
            if text.lower() == 'run test':
                run_program(program)
                continue
            if text.lower().startswith('run '):
                filename = text[4:].strip()
                run_file(filename)
                continue
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
        print(tree)
        result = interpreter.interpret(tree)
        print(result)
        if debug_mode:
            print("Interpreter current env:\n", interpreter.env)
    except ParserError as e:
        print(f"Parser Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def run_program(program_text):
    interpreter = Interpreter()
    lexer = Lexer(program_text)
    parser = Parser(lexer)
    try:
        ast = parser.parse()
        for statement in ast:
            result = interpreter.interpret(statement)
            print(result)
    except Exception as e:
        print(f"Error executing program: {e}")


def run_file(filename):
    try:
        with open(filename, 'r') as file:
            program_text = file.read()
        run_program(program_text)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error reading or executing file: {e}")


program = """
Defun { add, (x, y) } x + y
add(5, 3)
Lambd x,y.(x*y + 5)(3, 4)
"""

if __name__ == '__main__':
    main()