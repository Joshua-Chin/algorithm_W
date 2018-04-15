from w.parse import parse
from w.infer import infer

def typeof(string):
    return infer(parse(string))
