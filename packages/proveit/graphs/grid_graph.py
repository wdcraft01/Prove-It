from proveit import Function, Literal
from proveit import e, w, E, G, V
from proveit.logic import ClassMembership


class SquareGridGraph(Function):
    '''
    SquareGridGraph(m, n) represents a particular kind of lattice
    graph called a square-grid graph, with vertices corresponding to
    points (x, y) with integer coordinates (i.e. lattice points),
    with y coordinates in the range 1, 2,...,m (m is sometimes called
    its height) and x coordinates in the range 1, 2,..., n (n is
    sometimes called its width), with any two vertices being connected
    by an edge if and only if the corresponding points are one unit
    distance from each other. (See the Wikipedia entry on lattice
    graphs at https://en.wikipedia.org/wiki/Lattice_graph .)
    Internally, SquareGridGraph(m,n) is defined as a Graph in the
    following way:

        SquareGridGraph(m, n)
          = Graph(SquareGridPoints(m, n), SquareGridEdges(m, n))

    with SquareGridPoints and SquareGridEdges classes defined
    further below.

    This class is intended as a defining/enclosing super-graph of
    any graph representation of a Kitaev-style surface code. Thus
    GraphOf(K(m, n)) subseteq SquareGridGraph(m,n).
    '''

    # the literal operator of the SquareGridGraph operation
    _operator_ = Literal(string_format='SqGridGraph',
                         latex_format=r'\textrm{SqGridGraph}',
                         theory=__file__)

    def __init__(self, m, n, *, styles=None):
        '''
        Represent a square grid graph, SquareGridGraph(m,n) with
        vertex set V = {(x, y)}_{x in 1..n, y in 1..m} and edge set
        {{v1, v2} | d(v1, v2)=1}_{v1, v2 in V} (for m,n in NaturalPos).
        '''
        self.vertex_set = SquareGridPoints(m, n)
        # self.edge_set   = SetOfAll({v1, v2}) # under construction
        Function.__init__(
                self, SquareGridGraph._operator_, (m, n), styles=styles)


class SquareGridPoints(Function):
    '''
    SquareGridPoints(m, n) represents the set of 2D lattice points
    {(x, y)}_{x in 1..n, y in 1..m} (notice that m is the _vertical_
    bound, setting the limit for the _y_ values)
    '''

    # the literal operator of the SquareGridPoints operation
    _operator_ = Literal(string_format='SqGridPoints',
                         latex_format=r'\textrm{SqGridPoints}',
                         theory=__file__)

    def __init__(self, m, n, *, styles=None):
        '''
        Represent SquareGridPoints(m, n), the set of 2D lattice points
        in the plane given by {(x, y)}_{x in 1..n, y in 1..m}.
        '''
        self.m = m
        self.n = n
        Function.__init__(
                self, SquareGridPoints._operator_, (m, n), styles=styles)

    def membership_object(self, element):
        from .grid_graph_membership import SquareGridPointsMembership
        return SquareGridPointsMembership(element, self)

    @property
    def is_proper_class(self):
        '''
        The set of vertices of an m x n square grid graph is a set.
        This indicates that InSet() should be used instead of
        InClass() when GridPoints(m, n) is a domain.
        '''
        return False


class SquareGridEdges(Function):
    '''
    SquareGridEdges(m, n) represents the set of edges of an m x n
    square grid graph (itself represented by SquareGridGraph(m, n)).
    2D lattice points. This edge set consists of all the vertical
    and horizontal edges between adjacent lattice points in the set
    of square grid points:

        {{v1, v2} | d(v1, v2)=1}_{v1, v2 in SquareGridPoints(m, n)}.

    Notice that m is the _vertical_ bound, setting the limit for
    the _y_ values, and n is the _horizontal_ bound, setting the limit
    for the _x_ values.
    '''

    # the literal operator of the SquareGridEdges operation
    _operator_ = Literal(string_format='SqGridEdges',
                         latex_format=r'\textrm{SqGridEdges}',
                         theory=__file__)

    def __init__(self, m, n, *, styles=None):
        '''
        Represent SquareGridEdges(m, n), the set of edges in the
        m x n square grid graph SquareGridGraph(m, n).
        '''
        self.m = m
        self.n = n
        Function.__init__(
                self, SquareGridEdges._operator_, (m, n), styles=styles)

    def membership_object(self, element):
        from .grid_graph_membership import SquareGridEdgesMembership
        return SquareGridEdgesMembership(element, self)

    @property
    def is_proper_class(self):
        '''
        The set of edges of an m x n square grid graph is a set.
        This indicates that InSet() should be used instead of
        InClass() when SquareGridEdges(m, n) is the domain.
        '''
        return False


class GridGraphsLiteral(Literal):
    '''
    GridGraphs represents a generalized version of a class of graphs
    known in graph theory as grid graphs or square grid graphs,
    themselves being special cases of what are commonly called
    lattice graphs (see the Wikipedia entry on lattice graphs at
    https://en.wikipedia.org/wiki/Lattice_graph). In Prove-It,
    an element of the GridGraphs class is a graph in which all
    vertices are 2D lattice points (i.e. they have 2D integer
    coordinates), and all edges are of length 1 and always run either
    vertically or horizontally between nearest-neighbor vertices.
    This should be enough to capture a critical characteristic in
    such graphs: any path between vertices v1 and v2 will have a
    path length or weight greater than or equal to the Manhattan
    distance between vertices v1 and v2.
    This is also general enough to include the graphs corresponding
    to surface code configurations during the virtual rotation
    steps of a logical Hadamard.
    GridGraphs is a proper sub-class of the class of Graphs.

    UNDER DEVELOPMENT and probably not needed, but keeping here
    for a while longer while alternatives being developed.
    '''

    # the literal string for representing the class of GridGraphs
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='GridGraphs', 
                         latex_format=r'\textrm{GridGraphs}',
                         styles=styles)

    def membership_object(self, element):
        from .grid_graph_membership import GridGraphsMembership
        return GridGraphsMembership(element, self)

    @property
    def is_proper_class(self):
        '''
        The class of GridGraphs is a proper class (i.e., instead of a
        set). This indicates that InClass() should be used instead of
        InSet() when GridGraphs is a domain.
        '''
        return True



