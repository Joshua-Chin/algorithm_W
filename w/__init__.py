from w.parse import parse
from w.infer import infer, InferenceError

def typeof(string):
    return infer(parse(string))
