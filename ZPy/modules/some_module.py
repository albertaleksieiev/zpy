
import math
def square(a):
    return a * a


def square_from_pipe(zpy_input):
    return square(zpy_input)


def power(base, exponent=None):
    if exponent is None:
        def currying_function(zpy_input):
            return math.pow(base, zpy_input)

        return currying_function
    else:
        return math.pow(base, exponent)

