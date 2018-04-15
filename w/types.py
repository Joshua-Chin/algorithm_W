from functools import namedtuple

literal = namedtuple('literal', ['value'])
variable = namedtuple('variable', ['name'])
function = namedtuple('function', ['arg', 'result'])
polymorphic = namedtuple('polymorphic', ['bound_types', 'type'])
