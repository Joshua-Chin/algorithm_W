import ast
from lark import Lark, InlineTransformer
from w.exprs import *

GRAMMAR = r'''
expr: "(" expr ")"                      -> parens
    | "if" expr "then" expr "else" expr -> cond 
    | "let" VAR "=" expr "in" expr      -> let
    | "\\" VAR "->" expr                -> function
    | expr "==" expr                    -> equals
    | expr "!=" expr                    -> not_equal
    | expr "+" expr                     -> plus
    | expr "-" expr                     -> minus
    | expr "*" expr                     -> multiply
    | expr "/" expr                     -> divide    
    | expr expr                         -> call
    | "True"                            -> true
    | "False"                           -> false
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
    
    def equals(self, left, right):
        return call(call(variable('equals'), left), right)

     def not_equal(self, left, right):
        return call(call(variable('not_equal'), left), right)       

    def plus(self, left, right):
        return call(call(variable('plus'), left), right)

    def minus(self, left, right):
        return call(call(variable('minus'), left), right)

    def multiply(self, left, right):
        return call(call(variable('multiply'), left), right)

    def divide(self, left, right):
        return call(call(variable('divide'), left), right)

    def call(self, function, arg):
        return call(function, arg)

    def true(self):
        return literal(True)

    def false(self):
        return literal(False)

    def int(self, value):
        return literal(ast.literal_eval(value))

    def string(self, value):
        return literal(ast.literal_eval(value))

    def variable(self, name):
        return variable(str(name))

def parse(string):
    return T().transform(l.parse(string))
