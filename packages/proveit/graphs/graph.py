from proveit import equality_prover, Function, Literal, prover
from proveit import e, w, E, G, V
from proveit.logic import ClassMembership
# from proveit.graphs import GraphsMembership


class GraphsLiteral(Literal):
    '''
    Graphs represents the (mathematical) class of graphs, to which
    any specific graph G = (V, E) of vertices and edges belongs.
    This class might not be necessary, but is modeled on the
    HilbertSpacesLiteral class in the linear_algebra/inner_products
    theory package, and something similar involving the EmptySet in
    logic/sets. 'Graphs' is then defined in the graphs/common nb
    as Graphs = GraphsLiteral(). This class of graphs includes both
    finite and infinite graphs, but is initially conceptualized as
    the class of simple graphs (i.e. no loops and no parallel edges).
    See FiniteGraphsLiteral() for the class of finite graphs.
    '''

    # the literal string for representing the class of Graphs
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='Graphs', 
                         latex_format=r'\textrm{Graphs}',
                         styles=styles)

    def membership_object(self, element):
        from .graph_membership import GraphsMembership
        return GraphsMembership(element, self)

    @property
    def is_proper_class(self):
        '''
        The class of Graphs is a proper class (i.e., instead of a set).
        This indicates that InClass() should be used instead of
        InSet() when this is a domain.
        '''
        return True


class FiniteGraphsLiteral(Literal):
    '''
    FiniteGraphsLiteral() represents the (mathematical) class of
    finite graphs (i.e., graphs with a finite set of vertices and
    a finite set of edges), to which any specific finite graph
    G = (V, E) of vertices and edges belongs. This class of graphs
    is initially conceptualized as the class of simple finite graphs
    (i.e. no loops and no parallel edges).
    The string 'FiniteGraphs' is then defined in the graphs/common nb
    as FiniteGraphs = FiniteGraphsLiteral(), and should be imported
    from there.
    '''

    # the literal string for representing the class FiniteGraphs
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='FiniteGraphs', 
                         latex_format=r'\textrm{FiniteGraphs}',
                         styles=styles)

    def membership_object(self, element):
        return FiniteGraphsMembership(element, self)

    @property
    def is_proper_class(self):
        '''
        The class of finite graphs is a proper class (i.e. instead
        of a set). This method is used to indicates that InClass()
        should be used instead of InSet() when FiniteGraphs is being
        used as a domain.
        '''
        return True


class Graph(Function):
    '''
    Graph(V, E) represents a graph with vertex set V and edge set E.
    The vertex set V is conceptualized as a set of vertices such as
    {x_1, ..., x_n} but might appear or be interpreted as a set of
    geometric points such as {(x1, y1), (x2, y2), ..., (xn, yn)}.
    The edge set E is conceptualized as a set of pairs of vertices,
    such as {x1 x2, x2 x3, ..., xn x1}, which might eventually take
    the form of a set of 2-element sets or a set of ordered pairs.
    '''

    # the literal operator of the Graph operation
    _operator_ = Literal(string_format='Graph',
                         latex_format=r'\textrm{Graph}',
                         theory=__file__)

    def __init__(self, V, E, *, styles=None):
        '''
        Create a graph G(V,E) with vertex set V and edge set E.
        '''
        self.vertices = V
        self.edges   = E
        Function.__init__(
                self, Graph._operator_, (V, E), styles=styles)


class Order(Function):
    '''
    Order(G), denoted |G|, represents the order of graph G, giving
    the number of vertices in graph G. This will be equivalent to
    |Vertices(G)|.
    '''
    # literal operator of the Order operation.
    _operator_ = Literal(string_format='Order', theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent Order(G), the order of graph G, equivalent
        to the number of vertices in G.
        '''
        self.graph = G
        Function.__init__(
                self, Order._operator_, G, styles=styles)

    def string(self, **kwargs):
        return '|' + self.operand.string() + '|'

    def latex(self, **kwargs):
        return r'\left|' + self.operand.latex() + r'\right|'

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = |G|, deduce and return the equality:
        |G| = |Vertices(G)|.
        '''
        from . import graph_order_def
        _G_sub = self.operand
        return graph_order_def.instantiate({G:_G_sub}, auto_simplify=False)


class Size(Function):
    '''
    Size(G), denoted ||G||, represents the size of graph G, meaning
    the number of edges in graph G. This will be equivalent to
    |Edges(G)|.
    '''
    # literal operator of the Size operation.
    _operator_ = Literal(string_format='Size', theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent Size(G), the size of graph G, equivalent
        to the number of edges in G.
        '''
        self.graph = G
        Function.__init__(
                self, Size._operator_, G, styles=styles)

    def side_effects(self, judgment):
        '''
        Yield side-effects when representing 'Size(G)'.
        '''
        yield self.derive_size_in_natural

    def string(self, **kwargs):
        return '||' + self.operand.string() + '||'

    def latex(self, **kwargs):
        return r'\left\|' + self.operand.latex() + r'\right\|'

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = ||G||, deduce and return the equality:
        ||G|| = |Edges(G)|.
        '''
        from . import graph_size_def
        _G_sub = self.operand
        return graph_size_def.instantiate({G:_G_sub}, auto_simplify=False)

    @prover
    def derive_size_in_natural(self, **defaults_config):
        from . import graph_size_in_natural
        _G      = self.operand
        return (graph_size_in_natural.instantiate(
            {G:_G}, auto_simplify=False))


class EdgeWeight(Function):
    '''
    EdgeWeight(e, G) represents the weight of edge e in graph G.
    Prove-It complains if we reuse operators, so we use the operator
    w_{e} for the EdgeWeight operation and w_{g} for the GraphWeight
    operation (see further below).
    '''

    # literal operator of the EdgeWeight operation.
    _operator_ = Literal(string_format='w_e',
                         latex_format=r'w_{e}',
                         theory=__file__)

    def __init__(self, e, G, *, styles=None):
        '''
        Represent EdgeWeight(e, G), the weight of edge e in graph G.
        '''
        self.edge = e
        self.graph = G
        Function.__init__(
                self, EdgeWeight._operator_, (e, G), styles=styles)

    @prover
    def derive_in_real(self, **defaults_config):
        from . import edge_weight_in_real
        _e_sub = self.operands[0]
        _G_sub = self.operands[1]
        return (edge_weight_in_real.instantiate(
            {e:_e_sub, G:_G_sub}, auto_simplify=False))

class GraphWeight(Function):
    '''
    GraphWeight(G, w) represents the weight of graph G using edge-
    weighting function w, defined as the sum of the graph's edge
    weights using the edge-weighting function w:

        GraphWeight(G, w) = Sum (w(e)) for e in Edges(G).

    Prove-It complains if we reuse operators, so we use the operator
    w_{g} for the GraphWeight operation and w_{e} for the EdgeWeight
    operation.
    '''

    # literal operator of the GraphWeight operation.
    _operator_ = Literal(string_format='wgt',
                         latex_format=r'wgt',
                         theory=__file__)

    def __init__(self, G, w, *, styles=None):
        '''
        Represent GraphWeight(G), the weight of graph G.
        '''
        self.graph = G
        self.weight_fxn = w
        Function.__init__(
                self, GraphWeight._operator_, (G, w), styles=styles)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = GraphWeight(G, w), deduce and return the equality:
        GraphWeight(G, w) = Sum[w(e)] for e in Edges(G).
        '''
        from . import graph_weight_def
        _G_sub = self.operands[0]
        _w_sub = self.operands[1]
        return graph_weight_def.instantiate(
                {G:_G_sub, w:_w_sub}, auto_simplify=False)

    @prover
    def derive_in_real(self, **defaults_config):
        from . import graph_weight_in_real
        _G_sub = self.operands[0]
        _w_sub = self.operands[1]
        return (graph_weight_in_real.instantiate(
            {G:_G_sub, w:_w_sub}, auto_simplify=False))


class EdgeWeightFxns(Function):
    '''
    EdgeWeightFxns(G) represents the set of all possible
    edge-weighting functions on the graph G. An edge-weighting
    function is a mapping

        w: Edges(G) -> Values

    from the edges of G to some set of numeric values.
    This is less general than an edge-labeling function, and called
    an edge-weighting function to keep open the possibility of
    having analogous vertex-weighting or vertex-labeling functions.
    '''

    # the literal string operator for representing the set of weight
    # functions of a graph.
    _operator_ = Literal(string_format='EdgeWeightFxns',
                         latex_format=r'\textrm{EdgeWeightFxns}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent EdgeWeightFxns(G), the set of possible edge-weighting
        functions on graph G.
        '''
        self.graph = G
        Function.__init__(
                self, EdgeWeightFxns._operator_, G, styles=styles)

    def membership_object(self, element):
        from .weight_fxn_membership import EdgeWeightFxnsMembership
        return EdgeWeightFxnsMembership(element, self)

    @property
    def is_proper_class(self):
        '''
        The collection of possible weight functions on graph G is
        a set (instead of needing a proper class designation).
        This indicates that InSet() should be used instead of
        InClass() when this is a domain.
        '''
        return False


class Connected(Function): # IsConnected() is_connected() as literal op
    '''
    Connected(G) is a propositional function (or predicate)
    representing the claim that graph G is connected (i.e., that
    for every pair (u, v) of vertices in G, there exists a u-v path
    in G).
    '''

    # the literal operator of the Connected operation
    _operator_ = Literal(string_format='Connected',
                         latex_format=r'\textrm{Connected}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent the propositional function Connected(G),
        claiming graph G is connected.
        '''
        self.graph = G
        Function.__init__(
                self, Connected._operator_, G, styles=styles)
    
    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = Connected(G), deduce and return the equality:
        Connected(G) = A, where A represents the statement that,
        for all vertices u, v in G, there exists a u-v path in G.
        '''
        from . import connected_def
        _G_sub = self.operand
        return connected_def.instantiate({G:_G_sub}, auto_simplify=False)


class HasEulerianTrail(Function): # IsEulerian
    '''
    HasEulerTrail(G) is a propositional function (or predicate)
    claiming that graph G has an Eulerian trail (i.e., G has a
    walk that uses each and every edge of G exactly once).
    '''

    # the literal operator of the HasEulerTrail operation
    _operator_ = Literal(string_format='HasEulerianTrail',
                         latex_format=r'\textrm{HasEulerianTrail}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent the propositional function HasEulerianTrail(G),
        claiming graph G has an Eulerian trail.
        '''
        self.graph = G
        Function.__init__(
                self, HasEulerianTrail._operator_, G, styles=styles)


class HasEulerianCircuit(Function):
    '''
    HasEulerCircuit(G) is a propositional function (or predicate)
    claiming that graph G has an Eulerian circuit (i.e., G has a
    closed walk that uses each and every edge of G exactly once).
    '''

    # the literal operator of the HasEulerCircuit operation
    _operator_ = Literal(string_format='HasEulerianCircuit',
                         latex_format=r'\textrm{HasEulerianCircuit}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Represent the propositional function HasEulerianCircuit(G),
        claiming graph G has an Eulerian circuit.
        '''
        self.graph = G
        Function.__init__(
                self, HasEulerianCircuit._operator_, G, styles=styles)

