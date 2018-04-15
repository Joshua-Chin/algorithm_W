from lark import Lark, InlineTransformer
import w.exprs as exprs

GRAMMAR = r'''
start: expr
expr: "(" expr ")"                  -> parens
    | SIGNED_INT                    -> int
    | ESCAPED_STRING                -> string
    | VAR                           -> variable
    | "let" VAR "=" expr "in" expr  -> let
    | expr expr                     -> call
    | "\\" VAR "->" expr            -> function

%import common.SIGNED_INT
%import common.ESCAPED_STRING
%import common.WORD -> VAR
%import common.WS

%ignore WS
'''

l = Lark(GRAMMAR, parser='lalr', lexer='standard')

class T(InlineTransformer):

    def start(self, expr):
        return expr
    
    def parens(self, expr):
        return expr

    def int(self, value):
        return exprs.literal(int(value))

    def string(self, value):
        return exprs.literal(value.decode('unicode-escape'))

    def variable(self, name):
        return exprs.variable(str(name))
    
    def let(self, var, value, body):
        return exprs.let(exprs.variable(str(var)), value, body)

    def function(self, arg, body):
        return exprs.function(exprs.variable(str(arg)), body)

    def call(self, function, arg):
        return exprs.call(function, arg)

def parse(string):
    return T().transform(l.parse(string))
