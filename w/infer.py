from multipledispatch import dispatch

import w.exprs as exprs
import w.types as types
from w.disjointset import DisjointSet

class Environment(object):

    def __init__(self):
        self._types = DisjointSet()
        self._typings = {}
        self._typevars = 0


    def typeof(self, expr):
        """Returns the generalized type of an expression"""
        return self.generalize(self.w(expr))

    @dispatch(exprs.literal)
    def w(self, literal):
        """Returns the type of an expression"""
        # literals have a fixed type
        return types.literal(type(literal.value))

    @dispatch(exprs.variable)
    def w(self, variable):
        # variables have a type that depending on the environment
        return self.find(self.specialize(self._typings[variable]))

    @dispatch(exprs.call)
    def w(self, call):
        function = self.w(call.function)
        arg = self.w(call.arg)
        result = self.newvar()
        self.unify(function, types.function(arg, result))
        return self.find(result)

    @dispatch(exprs.function)
    def w(self, function):
        arg = self.newvar()
        self._typings[function.arg] = arg
        body = self.w(function.body)
        return types.function(self.find(arg), body)

    @dispatch(exprs.let)
    def w(self, let):
        # insert expr.var into typings to allow recursion
        var = self.newvar()
        self._typings[let.var] = var
        # compute type of value and unify it with var
        value = self.w(let.value)
        self.unify(var, value)
        # generalize the type of var
        self._typings[let.var] = self.generalize(self.find(var))
        return self.w(let.body)


    def newvar(self):
        """Returns a new type variable unique within the environment"""
        self._typevars += 1
        return types.variable('a' + str(self._typevars))


    @dispatch(types.literal)
    def find(self, literal):
        """Finds a representation of the type"""
        return literal

    @dispatch(types.variable)
    def find(self, variable):
        type = self._types.find(variable)
        return type if type == variable else self.find(type)

    @dispatch(types.function)
    def find(self, function):
        return types.function(
            self.find(function.arg),
            self.find(function.result))


    @dispatch(object)
    def specialize(self, type):
        """Specializes a polymorphic type into a monomorphic one"""
        return self.specialize(type, {})

    @dispatch(types.literal, object)
    def specialize(self, literal, subs):
        # type literals are already monomorphic
        return literal

    @dispatch(types.variable, object)
    def specialize(self, variable, subs):        
        # type variables may be polymorphic within a context
        return subs.get(variable, variable)
        
    @dispatch(types.function, object)
    def specialize(self, function, subs):
        arg = self.specialize(function.arg, subs)
        result = self.specialize(function.result, subs)
        return types.function(arg, result)

    @dispatch(types.polymorphic, object)
    def specialize(self, polymorphic, subs):
        # polymorphic forms are clearly polymorphic
        subs.update({
            bound_type: self.newvar()
            for bound_type in polymorphic.bound_types
        })
        return self.specialize(polymorphic.type, subs)


    def unify(self, x, y):
        """Unifies two types"""
        x = self.find(x)
        y = self.find(y)
        # if they are equal, they are already unified.
        if x == y:
            pass
        # if both are functions, they can be unified
        elif isinstance(x, types.function) and \
           isinstance(y, types.function):
            self.unify(x.arg, y.arg)
            self.unify(x.result, y.result)
        # if either is a type variable, they can be unified
        elif isinstance(x, types.variable) or \
             isinstance(y, types.variable):
            # ensure that `y` is a type variable
            if isinstance(x, types.variable):
                x, y = y, x
            # check for infinite types
            if y in self.free_types(x):
                raise TypeError(f'unifying {x} and {y} will result in an infinite type')
            self._types.merge(x, y)
        else:
            raise TypeError(f'{x} and {y} cannot be unified')


    def generalize(self, type):
        """Attempts to generalize a monomorphic type into a polymorphic one"""
        free_types = self.free_types(type)
        if not free_types: return type
        return types.polymorphic(free_types, type)

    @dispatch(types.literal)
    def free_types(self, literal):
        return frozenset()

    @dispatch(types.variable)
    def free_types(self, variable):
            return frozenset({variable})

    @dispatch(types.function)
    def free_types(self, function):
            return self.free_types(function.arg) | \
                   self.free_types(function.result)

def infer(expr):
    return Environment().typeof(expr)
