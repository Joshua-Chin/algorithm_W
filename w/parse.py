import ast
from lark import Lark, InlineTransformer
from w.exprs import *

GRAMMAR = r'''
start: expr
expr: "(" expr ")"                      -> parens
    | "if" expr "then" expr "else" expr -> cond 
    | "let" VAR "=" expr "in" expr      -> let
    | "\\" VAR "->" expr                -> function
    | expr expr                         -> call
    | SIGNED_INT                        -> int
    | ESCAPED_STRING                    -> string
    | VAR                               -> variable

%import common.SIGNED_INT
%import common.ESCAPED_STRING
%import common.WORD -> VAR
%import common.WS

%ignore WS
'''

l = Lark(GRAMMAR, parser='lalr', lexer='standard', start='expr')

class T(InlineTransformer):

    def start(self, expr):
        return expr
    
    def parens(self, expr):
        return expr

    def cond(self, cond, e1, e2):
        f = variable('if')
        f = call(f, cond)
        f = call(f, e1)
        f = call(f, e2)
        return f
    
    def let(self, var, value, body):
        return let(variable(str(var)), value, body)

    def function(self, arg, body):
        return function(variable(str(arg)), body)

    def call(self, function, arg):
        return call(function, arg)

    def int(self, value):
        return literal(ast.literal_eval(value))

    def string(self, value):
        return literal(ast.literal_eval(value))

    def variable(self, name):
        return variable(str(name))

def parse(string):
    return T().transform(l.parse(string))
