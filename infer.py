from functools import namedtuple

from union_find import UnionFind
from data import *


class Environment(object):

    def __init__(self):
        self._types = UnionFind()
        self._typings = {}
        self._typevar_index = 0

    def infer_type(self, expr):
        """
        Infers the type of an expression.
        """
        return self.generalize(self._infer_type(expr))

    def _infer_type(self, expr):
        # literals have known type
        if isinstance(expr, literal):
            return type_literal(type(expr.value))
        # variables have a type depending on the environment
        elif isinstance(expr, variable):
            return self.specialize(self._types.find(self._typings[expr]))
        # function calls require unifying the argument and the function
        elif isinstance(expr, call):
            functype = self._infer_type(expr.function)
            argtype = self._infer_type(expr.arg)
            result_type = self.newvar()
            self.unify(functype, function_type(argtype, result_type))
            return self._types.find(result_type)
        # function definition
        elif isinstance(expr, function):
            argtype = self.newvar()
            self._typings[expr.arg] = argtype
            body_type = self._infer_type(expr.body)
            return function_type(self._types.find(argtype), body_type)
        elif isinstance(expr, let):
            vartype = self.newvar()
            self._typings[expr.var] = vartype
            valuetype = self._infer_type(expr.value)
            self.unify(vartype, valuetype)
            self._typings[expr.var] = self.generalize(self._types.find(vartype))
            return self._infer_type(expr.body)
        raise TypeError(f"Unrecognized expression type: {type(expr)}")

    def newvar(self):
        """
        Returns a new type variable unique within the environment.
        """
        self._typevar_index += 1
        return type_variable(self._typevar_index)

    def specialize(self, type_, substitions=None):
        """
        Specializes the type into a monomorphic form by substituting bound variables.
        """
        if substitions is None:
            substitions = {}
        # type literals are already monomorphic
        if isinstance(type_, type_literal):
            return type_
        # type variables may be polymorphic within a context
        elif isinstance(type_, type_variable):
            return substitions.get(type_, type_)
        # function_types may have polymorphic bodies
        elif isinstance(type_, function_type):
            arg = self.specialize(self._types.find(type_.arg), substitions)
            result = self.specialize(self._types.find(type_.result), substitions)
            return function_type(arg, result)
        # polymorphic forms are clearly polymorphic
        elif isinstance(type_, polymorphic_type):
            substitions.update({
                self._types.find(bound_type): self.newvar()
                for bound_type in type_.bound_types
            })
            return self.specialize(self._types.find(type_.type), substitions)
        else:
            raise TypeError(f"Unrecognized metatype: {type(type_)}")

    def unify(self, x, y, seen=None):
        """
        Unifies two types within the environment.
        """
        x = self._types.find(x)
        y = self._types.find(y)
        # if they are equal, they are already unified.
        if x == y:
            return
        # if both are functions, try to unify their arguments and results
        elif isinstance(x, function_type) and isinstance(y, function_type):
            self.unify(x.arg, y.arg)
            self.unify(x.result, y.result)
        # if either is a type variable, they can be unified
        elif isinstance(x, type_variable) or isinstance(y, type_variable):
            if x in self.free_types(y) or y in self.free_types(x):
                raise ValueError("Recursive type detected")
            self._types.unify(x, y)
        else:
            raise TypeError(f'type {x} and type {y} cannot be unified')

    def generalize(self, type_):
        """
        Generalizes a monomorphic type with free variables into a polymorphic form.
        """
        free_types = self.free_types(type_)
        if free_types:
            return polymorphic_type(self.free_types(type_), type_)
        else:
            return type_

    def free_types(self, type_):
        if isinstance(type_, type_literal):
            return frozenset()
        elif isinstance(type_, type_variable):
            return frozenset({self._types.find(type_)})
        elif isinstance(type_, function_type):
            return self.free_types(self._types.find(type_.arg)) | \
                self.free_types(self._types.find(type_.result))
        elif isinstance(type_, polymorphic_type):
            return self.free_types(self._types.find(type_.type)) - \
                {self._types.find(bound_type) for bound_type in type_.bound_types}
        raise TypeError(f"Unrecognized metatype: {type(type_)}")
