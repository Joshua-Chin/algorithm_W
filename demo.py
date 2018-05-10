from w import typeof, InferenceError
from lark import UnexpectedToken

if __name__ == '__main__':
    try:
        while True:
            try:
                print(typeof(input('> ')))
            except UnexpectedToken:
                print(f'Syntax Error')
            except InferenceError as e:
                print(f'Type Error: {e}')
    except KeyboardInterrupt:
        pass
