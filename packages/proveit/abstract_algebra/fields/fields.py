from proveit import Function, Literal

class Fields(Function):
    '''
    A Fields expression denotes the class of sets that are rings
    under particular "addition" and "multiplication" operations.
    '''
    
    _operator_ = Literal(
            string_format=r'Fields', latex_format=r'\textrm{Fields}',
            theory=__file__)
    
    def __init__(self, add_operator, mult_operator, *, styles=None):
        Function.__init__(self, Fields._operator_, 
                          (add_operator, mult_operator), 
                          styles=styles)

    @property
    def is_proper_class(self):
        '''
        This is a proper class. This indicates that
        InClass should be used instead of InSet when this is a domain.
        '''
        return True


class FiniteField(Function):
    '''
    FiniteField(n) represents the finite field (or Galois field)
    {0, 1, 2, ..., n-1}, where n = p^{k} for some prime p and
    positive integer k, and the operations are mod p^{k} addition
    and mod p^{k} multiplication.
    The representation itself does not check that the argument n
    supplied is indeed of the form p^{k}. Instead, the constraint
    would be applied at the time of usage in a theorem, etc., like
    this:

    THM: forall{p in prime} forall_{k in natpos},
         F(p^k) has some property, etc

    '''

    _operator_ = Literal(
            string_format=r'F', latex_format=r'\mathbb{F}',
            theory=__file__)

    def __init__(self, n, *, styles=None):
        self.order = n
        Function.__init__(self, FiniteField._operator_, n, styles=styles)

    def string(self, **kwargs):
        return self.formatted('string', **kwargs)

    def latex(self, **kwargs):
        return self.formatted('latex', **kwargs)

    def formatted(self, format_type, **kwargs):
        formatted_operator = self.operator.formatted(format_type, fence=False)
        formated_order = self.order.formatted(format_type, fence=False)
        if format_type == 'latex':
            return formatted_operator + '_{' + formated_order + '}'
        else:
            return 'F_{' + formated_order + '}'
