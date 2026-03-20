from proveit import Literal, Operation


class QuotientGraph(Operation):
    '''
    QuotientGraph(G, q) represents the quotient graph of G under
    the quotient mapping q: V(G)-> V(G)/~, i.e. the map q taking each
    vertex v of G to its equivalence class [v]. See the Wikipedia entry
    on quotient graphs at https://en.wikipedia.org/wiki/Quotient_graph.
    Setting H = QuotientGraph(G, q), i.e., setting H to be the
    quotient graph of G under the quotient map q, means that q is a
    surjective homomorphism from V(G) to V(H), with the graph
    "homomorphism" meaning that the mapping preserves adjacency:
    for any edge {u,v} in G, either {q(u), q(v)} is an edge in H or
    q(u) = q(v). The mapping is also edge-surjective, meaning that for
    any edge {x, y} in H, there must exist an edge {u, v} in G such
    that q(u)=x and q(v) = y.
    The text/latex representation for QuotientGraph(G, q) is G/q,
    analogous to quotient notation more generally.
    To make represent a generic quotient graph of G, without specifying
    the details of a quotient map q, the user can supply a generic
    variable, such as ~ or q, as a "name" for an unspecified or
    uncharacterized quotient mapping.
    '''

    # generic literal operator of the QuotientGraph() operation.
    _operator_ = Literal(string_format='QGraph',
                         latex_format=r'\textrm{QGraph}',
                         theory=__file__)

    def __init__(self, G, qmap, *, styles=None):
        '''
        Represent QuotientGraph(G, qmap), the quotient graph of G
        under the quotient mapping qmap.
        '''
        self.original_graph = G
        self.qmap = qmap
        super().__init__(self._operator_, (G, qmap), styles=styles)

    def string(self, **kwargs):
        return (self.original_graph.string() + "/" +
                    self.qmap.string())

    def latex(self, **kwargs):
        return (self.original_graph.latex() + r'/' +
                    self.qmap.latex())