# Algorithm W
This repository contains an implementation of Algorithm W, a fast type inference algorithm.

This implementation supports the syntax

- Let Expressions:
    - `let x = 3 in x`
- Lambda Expressions:
    - `\x -> x + 3`
- Function Calls 
    - `f x`
- If Expressions:
    - `if x then y else z`
- Literals:
    - `3`, `"abc"`, `True`

Here are some more complicated examples

### Factorial
```
> let fac = \x -> if x == 0 then 1 else x * fac (x - 1) in fac
<class 'int'> -> <class 'int'>
```

### Fibonacci Sequence
```
> let fib = \x -> if x == 0 then 0 else if x == 1 then 1 else fib (x - 1) + fib (x - 2) in fib
<class 'int'> -> <class 'int'>
```

Try it out with `python3 demo.py`
