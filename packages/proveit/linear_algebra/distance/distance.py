from proveit import Function, Literal


class MinkowskiDistance(Function):
    '''
    MinkowskiDistance(p, x, y) represents the Minkowski distance
    of order p between points x and y, also known as the L_{p}
    distance. This is axiomatically defined for two n-dimensional
    Real-component points x and y as:

        d_{p} = ( Sum |x_i - y_i|^{p} )^{1/p}

    for i in {1, 2, …, n}.
    '''

    # operator of the MinkowskiDistance operation.
    _operator_ = Literal(string_format='d_{p}',
                         latex_format=r'd_{p}',
                         theory=__file__)
    
    def __init__(self, p, x, y, *, styles=None):
        '''
        Initialize a representation of the Minkowski distance
        of order p between points x and y.
        '''
        self.order = p
        self.points = (x, y)
        Function.__init__(
                self, MinkowskiDistance._operator_,
                (p, x, y), styles=styles)

    def string(self, **kwargs):
        return ('d_{' + self.order.string() + '}('
                + self.operands[1].string() + ', '
                + self.operands[2].string() + ')')

    def latex(self, **kwargs):
        return (r'd_{' + self.order.latex() + r'}('
                + self.operands[1].latex() + r', '
                + self.operands[2].latex() + r')')


class ManhattanDistance(Function):
    '''
    ManhattanDistance(p, q) represents the Manhattan distance (also
    known as the L1 distance or more colloquially as the taxi cab
    distance) between points p and q. For 2-D points (x1, y1) and
    (x2, y2), we have:

        ManhattanDistance((x1,y1),(x2,y2)) = |x2-x1| + |y2-y1|
    '''

    # the literal operator of the ManhattanDistance function
    _operator_ = Literal(
            string_format='md', latex_format=r'd_{m}\!', theory=__file__)

    def __init__(self, pt1, pt2, *, styles=None):
        '''
        Create an expression representing the Manhattan or L1 distance
        between two points pt1 and pt2.
        '''
        Function.__init__(
                self, ManhattanDistance._operator_, (pt1, pt2),
                styles=styles)