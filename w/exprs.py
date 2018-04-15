from functools import namedtuple

literal = namedtuple('literal', ['value'])
variable = namedtuple('variable', ['name'])
function = namedtuple('function', ['arg', 'body'])
call = namedtuple('call', ['function', 'arg'])
let = namedtuple('let', ['var', 'value', 'body'])
