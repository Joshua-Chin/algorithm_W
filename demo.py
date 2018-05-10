from w import typeof, InferenceError
from lark import UnexpectedToken, UnexpectedInput

if __name__ == '__main__':
    try:
        while True:
            try:
                print(typeof(input('> ')))
            except (UnexpectedToken, UnexpectedInput) as e:
                print(f'Syntax Error: line {e.line}, col {e.column}')
            except InferenceError as e:
                print(f'Type Error: {e}')
    except KeyboardInterrupt:
        pass
