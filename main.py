from interpreter import Interpreter
from lexer import Lexer
from parserR import Parser, ParserError

def main():
    interpreter = Interpreter()

    while True:
        try:
            text = input('foo>> ')
            if text.lower() in ['exit', 'quit']:
                break
            if text.lower() in ['run test']:
                run_test(program)
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
            print("intepreter current env : \n",interpreter.env)
        except ParserError as e:
            print(f"Parser Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


def run_test(program_text):
    interpreter = Interpreter()
    lexer = Lexer(program_text)
    parser = Parser(lexer)
    ast = parser.parse()
    results = []
    for statement in ast:
        result = interpreter.interpret(statement)
        results.append(result)
        print(result)
    return results


program = """
Defun { add, (x, y) } x + y;
add(5, 3);
Lambd x,y.(x*y + 5)(3, 4);
"""

  

if __name__ == '__main__':
    main()
