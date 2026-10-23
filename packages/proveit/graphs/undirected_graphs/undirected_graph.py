from proveit import Function, Literal

class UndirectedGraph(Function):
    '''
    UndirectedGraph(V, E) represents an undirected graph with
    vertex set V and edge set E. The vertex set V is conceptualized as
    any set of relevant objects, and in axioms and theorems, etc.,
    vertices often appear as {v_1, ..., v_n} but might appear or be
    interpreted as a set of geometric points such as
    {(x1, y1), (x2, y2), ..., (xn, yn)}, etc.
    The edge set E is conceptualized as a set of 2-element subsets of
    vertices, such as {{v1, v2}, {v4, v5}, ...}. Such un-ordered
    edges distinguish undirected graphs from digraphs.
    Letting G = UndirectedGraph(V, E) is no guarantee that the (V, E)
    tuple represents a legitimate undirected graph (i.e., there is no
    check on the relationship between vertices in V and edges in E).
    '''

    # the literal operator of the UndirectedGraph operation
    _operator_ = Literal(string_format='UndirectedGraph',
                         latex_format=r'\textrm{UndirectedGraph}',
                         theory=__file__)

    def __init__(self, V, E, *, styles=None):
        '''
        Create an undirected graph G(V,E) with vertex set V and
        edge set E.
        '''
        self.vertices = V
        self.edges   = E
        Function.__init__(
                self, UndirectedGraph._operator_, (V, E),
                styles=styles)

