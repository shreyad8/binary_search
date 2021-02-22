#!/bin/python3

def find_smallest_positive(xs):
    '''
    Assume that xs is a list of numbers sorted from LOWEST to HIGHEST.
    Find the index of the smallest positive number.
    If no such index exists, return `None`.

    HINT:
    This is essentially the binary search algorithm from class,
    but you're always searching for 0.

    APPLICATION:
    This is a classic question for technical interviews.

    >>> find_smallest_positive([-3, -2, -1, 0, 1, 2, 3])
    4
    >>> find_smallest_positive([1, 2, 3])
    0
    >>> find_smallest_positive([-3, -2, -1]) is None
    True
    '''
    if len(xs)==0:
        return
    left = 0
    right = len(xs)-1
    def go(left,right):
        if left==right:
            if xs[left]>0:
                return left
            else:
                return None
        mid = (left+right)//2
        if xs[mid] > 0:
            right = mid
        if xs[mid] <= 0:
            left = mid+1
        return go(left,right)
    return go(left,right)


def count_repeats(xs, x):
    '''
    Assume that xs is a list of numbers sorted from HIGHEST to LOWEST,
    and that x is a number.
    Calculate the number of times that x occurs in xs.

    HINT:
    Use the following three step procedure:
        1) use binary search to find the lowest index with a value >= x
        2) use binary search to find the lowest index with a value < x
        3) return the difference between step 1 and 2
    I highly recommend creating stand-alone functions for steps 1 and 2,
    and write your own doctests for these functions.
    Then, once you're sure these functions work independently,
    completing step 3 will be easy.

    APPLICATION:
    This is a classic question for technical interviews.

    >>> count_repeats([5, 4, 3, 3, 3, 3, 3, 3, 3, 2, 1], 3)
    7
    >>> count_repeats([1, 2, 3], 4)
    0
    '''
    if len(xs)==0:
        return 0
    return _find_upper(xs,x) - _find_lower(xs,x)


def _find_lower(xs, x):
    left = 0
    right = len(xs)-1
    def go(left,right):
        if left==right:
            if xs[left]==x:
                return left
            else:
                return len(xs)
        mid = (left+right)//2
        if xs[mid] <= x:
            right = mid
        if xs[mid] > x:
            left = mid+1
        return go(left,right)
    return go(left,right)


def _find_upper(xs, x):
    left = 0
    right = len(xs)-1
    def go(left,right):
        if left==right:
            if xs[left]<x:
                return left
            else:
                return left+1
        mid = (left+right)//2
        if xs[mid] < x:
            right = mid
        if xs[mid] >= x:
            left = mid+1
        return go(left,right)
    return go(left,right)


def argmin(f, lo, hi, epsilon=1e-3):
    '''
    Assumes that f is an input function that takes a float as input and returns a float with a unique global minimum,
    and that lo and hi are both floats satisfying lo < hi.
    Returns a number that is within epsilon of the value that minimizes f(x) over the interval [lo,hi]

    HINT:
    The basic algorithm is:
        1) The base case is when hi-lo < epsilon
        2) For each recursive call:
            a) select two points m1 and m2 that are between lo and hi
            b) one of the 4 points (lo,m1,m2,hi) must be the smallest;
               depending on which one is the smallest,
               you recursively call your function on the interval [lo,m2] or [m1,hi]

    APPLICATION:
    Essentially all data mining algorithms are just this argmin implementation in disguise.
    If you go on to take the data mining class (CS145/MATH166),
    we will spend a lot of time talking about different f functions that can be minimized and their applications.
    But the actual minimization code will all be a variant of this binary search.

    WARNING:
    The doctests below are not intended to pass on your code,
    and are only given so that you have an example of what the output should look like.
    Your output numbers are likely to be slightly different due to minor implementation details.
    Writing tests for code that uses floating point numbers is notoriously difficult.
    See the pytests for correct examples.

    >>> argmin(lambda x: (x-5)**2, -20, 20)
    5.000040370009773
    >>> argmin(lambda x: (x-5)**2, -20, 0)
    -0.00016935087808430278
    '''

    m1 = lo + (hi-lo) / 3
    m2 = lo + (hi-lo) / 3 * 2

    assert(lo <= m1 <= m2 <= hi)

    if hi-lo < epsilon:
        return (hi+lo)/2

    f_lo = f(lo)
    f_m1 = f(m1)
    f_m2 = f(m2)
    f_hi = f(hi)

    f_min = min([f_lo,f_m1,f_m2,f_hi])

    if f_min==f_lo:
        return argmin(f, lo, m1, epsilon)

    if f_min==f_m1:
        return argmin(f, lo, m2, epsilon)

    if f_min==f_m2:
        return argmin(f, m1, hi, epsilon)

    if f_min==f_hi:
        return argmin(f, m2, hi, epsilon)


def find_boundaries(f):
    '''
    Returns a tuple (lo,hi).
    If f is a convex function, then the minimum is guaranteed to be between lo and hi.
    This function is useful for initializing argmin.

    HINT:
    Begin with initial values lo=-1, hi=1.
    Let mid = (lo+hi)/2
    if f(lo) > f(mid):
        recurse with lo*=2
    elif f(hi) < f(mid):
        recurse with hi*=2
    else:
        you're done; return lo,hi
    '''
    lo = -1
    mid = 0
    hi = 1
    f_lo = f(lo)
    f_mid = f(mid)
    f_hi = f(hi)
    
    while not (f_lo >= f_mid and f_mid <= f_hi):
        if f_lo < f_mid:
            lo_old = lo
            f_lo_old = f_lo
            lo *= 2
            f_lo = f(lo)
            mid = lo_old
            f_mid = f_lo_old
        else:
            hi_old = hi
            f_hi_old = f_hi
            hi *= 2
            f_hi = f(hi)
            mid = hi_old
            f_mid = f_hi_old

    return lo,hi


def argmin_simple(f, epsilon=1e-3):
    '''
    This function is like argmin, but it internally uses the find_boundaries function so that
    you do not need to specify lo and hi.
    '''
    lo,hi = find_boundaries(f)
    print("lo,hi=",lo,hi)
    return argmin(f, lo, hi, epsilon)

