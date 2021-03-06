from proveit import Context, Function,Literal

class GCD(Function):

    _operator_ = Literal('gcd', context=__file__)
    
    def __init__(self, a, b):
        Function.__init__(self, GCD._operator_, [a, b])