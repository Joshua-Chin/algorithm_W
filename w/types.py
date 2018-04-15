from functools import namedtuple

class literal(namedtuple('literal', ['value'])):
    def __repr__(self):
        return repr(self.value)

class variable(namedtuple('variable', ['name'])):
    def __repr__(self):
        return self.name

class function(namedtuple('function', ['arg', 'result'])):
    def __repr__(self):
        if isinstance(self.arg, (literal, variable)):
            return f'{repr(self.arg)} -> {repr(self.result)}'
        return f'({repr(self.arg)}) -> {repr(self.result)}'

class polymorphic(namedtuple('polymorphic', ['bound_types', 'type'])):
    def __repr__(self):
        return f'forall {", ".join(repr(type) for type in self.bound_types)} . {repr(self.type)}'
