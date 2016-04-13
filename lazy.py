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

def nats():
    """
>>> list(take(10, nats()))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    return iterate(lambda x: x + 1, 0)

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
        yield f(next(xs), next(ys))

def fibs():
    """
>>> list(take(10, fibs()()))
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    def go():
        nonlocal mgo
        yield 0
        yield 1
        for f in zip_with(lambda x, y: x + y, mgo(), tail(mgo())):
            yield f

    mgo = memo(go())

    return mgo

def memo(xs):
    """
>>> g = memo(example())
>>> list(g())
[1, 2, 3]
>>> list(g())
[1, 2, 3]

    """
    stored = []

    def go():
        nonlocal xs, stored
        for i in stored:
            yield i
        for x in xs:
            stored.append(x)
            yield x

    return go

def append(xs, ys):
    """
>>> list(append([1,2,3], [4,5,6]))
[1, 2, 3, 4, 5, 6]
>>> list(take(6, append([1,2,3], repeat('a'))))
[1, 2, 3, 'a', 'a', 'a']
    """
    for x in xs:
        yield x
    for y in ys:
        yield y

def filter(p, xs):
    """
>>> list(take(5, filter(lambda x: x % 2 == 0, nats())))
[0, 2, 4, 6, 8]
    """
    for x in xs:
        if p(x):
            yield x

def partition(p, xs):
    mxs = memo(xs)
    def left():
        nonlocal p, mxs
        for x in mxs():
            if p(x):
                yield x

    def right():
        nonlocal p, mxs
        for x in mxs():
            if not p(x):
                yield x

    return left, right

def uncons(xs):
    return head(xs), tail(xs)

def qsort(xs):
    """
in Haskell,

    qsort (x:xs) = qsort lesser ++ [x] ++ qsort greater 
      where
        (lesser, greater) = partition (<x) xs

>>> list(qsort(cons(1, nil)))
[1]
>>> list(qsort(iter(nil)))
[]
>>> list(qsort(iter([1, 2])))
[1, 2]
>>> list(qsort(iter([2, 1])))
[1, 2]
>>> list(qsort(iter([4,2,3,1])))
[1, 2, 3, 4]
    """
    x = next(xs)
    lesser, greater = partition(lambda n: n < x, xs)
    
    for r in qsort(lesser()):
        yield r

    yield x

    for r in qsort(greater()):
        yield r

import doctest

doctest.testmod()
