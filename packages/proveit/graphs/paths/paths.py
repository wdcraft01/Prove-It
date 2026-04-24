from proveit import Function, Literal, NamedExprs, Operation
from proveit.logic import ClassMembership
from proveit.graphs import Graph

class Paths(Literal):
    '''
    Paths() represents the set of all graphs that are (undirected)
    paths. A undirected path is a non-empty graph P = (V,E)
    with non-empty vertex set V and (possibly empty) edge set E such
    that:
            V = {x0, x1, ..., xk},
            E = {{x0,x1}, {x1,x2}, ..., {x_{k-1},x_{k}},

    where the x_{i} are all distinct. The vertices x0 and xk are said
    to be linked by the path P and are called its endvertices, or
    endpoints, or simply its ends. The vertices x1, ..., x_{k-1} are
    the inner vertices of P. The number of edges in the path P,
    denoted ||P||, is its length (in this example, ||P|| = k).
    '''

    # the literal string for representing the class of Paths
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='Paths', 
                         latex_format=r'\textrm{Paths}',
                         styles=styles)

    @property
    def is_proper_class(self):
        '''
        Paths consitute a proper class (i.e. instead of a set).
        This indicates that InClass() should be used instead of
        InSet() when this is a domain.
        '''
        return True

    def membership_object(self, element):
        from .paths_membership import PathsMembership
        return PathsMembership(element, self)

    def nonmembership_object(self, element):
        from .paths_membership import PathsNonmembership
        return PathsNonmembership(element, self)


class Path(Graph):
    '''
    Path(V,E) represents the special type of graph called a path,
    with vertex set V and edge set E. A path is a non-empty graph
    P = (V,E) with vertex set V and (possibly empty) edge set E such
    that:

        V = {x0, x1, ..., xk},
        E = {{x0,x1}, {x1,x2}, ..., {x_{k-1},x_{k}}},

    where the x_{i} are all distinct. The vertices x0 and xk are said
    to be linked by the path P and are called its endvertices, or
    endpoints, or simply its ends. The vertices x1, ..., x_{k-1} are
    the inner vertices of P. The number of edges in the path P,
    denoted ||P||, is its length (in this example, ||P|| = k).
    '''

    # the literal operator of the Path operator
    _operator_ = Literal(string_format='Path',
                         latex_format=r'\text{Path}',
                         theory=__file__)

    def __init__(self, V, E, *, styles=None):
        '''
        Create or represent a path, Path(V,E), with vertex set V
        and edge set E. If explicit sets of vertices and edges are
        provided, they are NOT currently verified to represent a
        valid path.
        '''
        self.vertex_set = V
        self.edge_set   = E
        Function.__init__(self, Path._operator_, (V, E), styles=styles)


class IsPath(Operation):
    '''
    IsPath(P, G) denotes that P is a path in graph G.
    IsPath(P, G, a, b) denotes that P is a path in graph G with
    path endpoints a and b.
    Technically, a path P is not a graph but a sequence
        (v0, v1, ..., vn)
    of non-repeating adjacent vertices in the containing graph G.
    To deal with the graph of such a path, you will need PathGraph(P, G)
    with PathGraph(P, G) being a subgraph of graph G.
    '''

    # the literal operator of the IsPath operation
    _operator_ = Literal(string_format='IsPath',
                         latex_format=r'\text{IsPath}',
                         theory=__file__)

    def __init__(self, path, graph, start=None, end=None, *, styles=None):
        '''
        Represent the claim IsPath(P, G) that P is a path in graph G,
        or the more specific claim IsPath(P, G, a, b) that P is a path
        in G with path endpoints a and b.
        '''

        # (1) Build the list of (keyword, expression) pairs
        items = [
            ("path", path),
            ("graph", graph)
        ]
        
        # (2) Only add optional endpoints if they are actually provided
        if start is not None:
            items.append(("start", start))
        if end is not None:
            items.append(("end", end))
        
        # (3) Initialize NamedExprs with the list of tuples
        operands = NamedExprs(*items)
        
        # (4) Call Operation's init
        super().__init__(self._operator_, operands=operands, styles=styles)

    def string(self, **kwargs):
        string_str = ('IsPath(' + self.path.string() + ', ' +
                      self.graph.string())
        if (hasattr(self, 'start') and self.start is not None):
            string_str += ', ' + self.start.string()
        if (hasattr(self, 'end') and self.end is not None):
            string_str += ', ' + self.end.string()
        string_str += ')'
        return string_str

    def latex(self, **kwargs):
        latex_str = (r'\text{IsPath}(' + self.path.latex() + r', ' +
                     self.graph.latex())
        if (hasattr(self, 'start') and self.start is not None):
            latex_str += r', ' + self.start.latex()
        if (hasattr(self, 'end') and self.end is not None):
            latex_str += r', ' + self.end.latex()
        latex_str += r')'
        return latex_str

    @classmethod
    def extract_init_arg_value(cls, arg_name, operator, operands):
        # The base Operation.__init__ already maps keys to attributes 
        # via getattr/setattr, but for reconstruction (remaking exprs), 
        # we check the NamedExprs specifically.
        if isinstance(operands, NamedExprs):
            return operands.get(arg_name, None)
        return None

