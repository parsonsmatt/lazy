nil = []

def cons(x, xs):
    """
>>> for i in cons(1, nil): print(i)
1
>>> for i in cons(1, cons(2, cons(3, nil))): print(i)
1
2
3
    """
    yield x
    for i in xs:
        yield i

example = lambda: cons(1, cons(2, cons(3, nil)))

def head(xs):
    """
>>> print(head(example()))
1
>>> list(example())
[1, 2, 3]
    """
    return next(xs)

def drop(n, xs):
    """
>>> for i in drop(1, example()): print(i)
2
3
    """
    for i in range(0, n):
        next(xs)

    for x in xs:
        yield x

def tail(xs):
    """
>>> list(tail(example()))
[2, 3]
    """
    return drop(1, xs)

def take(n, xs):
    """
>>> list(take(2, example()))
[1, 2]
    """
    for i in range(0, n):
        yield next(xs)

def repeat(a):
    """
>>> list(take(3, repeat(3)))
[3, 3, 3]
    """
    return iterate(lambda x: x, a)

def iterate(f, a):
    """
>>> list(take(3, iterate(lambda x: x+1, 5)))
[5, 6, 7]
    """
    while True:
        yield a
        a = f(a)

def zip(xs, ys):
    """
>>> list(take(3, zip(repeat(1), repeat(2))))
[(1, 2), (1, 2), (1, 2)]
>>> list(take(3, zip(repeat(1), example())))
[(1, 1), (1, 2), (1, 3)]
>>> list(take(3, zip(example(), repeat(1))))
[(1, 1), (2, 1), (3, 1)]
    """
    return zip_with(lambda x, y: (x,y), xs, ys)

def zip_with(f, xs, ys):
    """
>>> list(take(3, zip_with(lambda x, y: x + y, repeat(1), repeat(2))))
[3, 3, 3]
    """
    while True:
        x = next(xs)
        y = next(ys)
        yield f(x,y)

def fibs():
    """
>>> list(take(10, fibs()))
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    yield 0
    yield 1
    for f in zip_with(lambda x, y: x + y, fibs(), tail(fibs())):
        yield f

import doctest

doctest.testmod()
