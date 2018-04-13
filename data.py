from functools import namedtuple

# expression values
literal = namedtuple('literal', ['value'])
variable = namedtuple('variable', ['name'])
function = namedtuple('function', ['arg', 'body'])
call = namedtuple('call', ['function', 'arg'])
let = namedtuple('let', ['var', 'value', 'body'])

# type values
type_literal = namedtuple('type_literal', ['value'])
type_variable = namedtuple('type_variable', ['name'])
function_type = namedtuple('function_type', ['arg', 'result'])
polymorphic_type = namedtuple('polymorphic', ['bound_types', 'type'])
