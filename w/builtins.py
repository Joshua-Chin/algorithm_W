from w.types import *
import w.exprs as exprs

num_binop = function(literal(int), function(literal(int), literal(int)))

typings = {
    exprs.variable('if'): polymorphic([variable('a')],
        function(literal(bool), function(variable('a'), function(variable('a'), variable('a'))))),
    exprs.variable('equals'): polymorphic([variable('a')],
        function(variable('a'), function(variable('a'), literal(bool)))),
    exprs.variable('not_equal'): polymorphic([variable('a')],
        function(variable('a'), function(variable('a'), literal(bool)))),
    exprs.variable('plus'): num_binop,
    exprs.variable('minus'): num_binop,
    exprs.variable('multiply'): num_binop,
    exprs.variable('divide'): num_binop,
}
