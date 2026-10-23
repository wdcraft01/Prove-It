from proveit import G, Function, Literal
from proveit import equality_prover, prover, ClassMembership
from proveit import f, A, B

class IsDigraph(ClassMembership):
    '''
    IsDigraph(G) is the class predicate claim that G is a digraph,
    and replaces the problematic conceptual approach of claiming that
    "G is in the class of Digraphs".
    For our purposes here, the class of digraphs will be understood to
    consist of finite simple graphs of the form (V,E), consisting of
    vertex set V and edge set E ("simple" here means no loops and no
    parallel edges). Some textbooks insist that V be non-empty, but
    until we run into problems, we will allow V to be empty (producing
    the "empty digraph" DG(EmptySet, EmptySet)).
    The claim IsGraph(G) then is tantamount to claiming that G is
    an ordered pair (V, E) of vertices V and edges E such that
    E is a subset of the Cartesian product V x V.
    '''
    _operator_ = Literal('IsDigraph', r'\textrm{IsDigraph}',
                         theory=__file__)
    
    def __init__(self, G, *, styles=None):
        ClassMembership.__init__(self, IsDigraph._operator_,
                                 G, styles=styles)
        self.graph = G

    def formatted_class(self, format_type):
        if format_type == 'latex':
            return r'{\textrm{Digraphs}}'
        return r'Digraphs'

    def side_effects(self, judgment):
        '''
        Yield side-effects when proving or assuming 'IsDigraph(G)':

            * IsGraph(G);
            * ||G|| in Natural (this assumes that G is finite);
            * Edges(G) 'subseteq' (Vertices(G) x Vertices(G))
        '''
        yield self.derive_is_graph
        yield self.derive_size_in_natural
        # yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Derive and return that

            IsDigraph(G) =
            Edges(G) 'subseteq' (Vertices(G) x Vertices(G))

        i.e., that G being a digraph means that its edges consist of
        a subset of the Cartesian product Vertices(G) x Vertices(G).
        '''
        from . import is_digraph_def
        _G_sub = self.graph
        return is_digraph_def.instantiate({G: _G_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From self=IsDigraph(G), return the expression (not a Judgment):
            Edges(G) 'subseteq' Vertices(G) x Vertices(G)
        i.e., that G being a digraph means that its edges consist of
        a subset of the set of 2-element ordered tuples of its vertices.
        '''
        from proveit.logic.sets import CartExp, SubsetEq
        from proveit.numbers import two
        from proveit.graphs import Edges, Vertices
        _G_sub = self.graph
        return SubsetEq(Edges(_G_sub), CartExp(Vertices(_G_sub), two))

    @prover
    def unfold(self, **defaults_config):
        '''
        From IsDigraph(G), derive and return:

            |- Edges(G) 'subseteq' (Vertices(G) x Vertices(G))

        i.e., that the edges of digraph G consist of a subset of the
        Cartesian product V x V of the vertex set V with itself.
        '''
        from . import is_digraph_unfolding
        _G_sub = self.graph
        return is_digraph_unfolding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Prove self = IsDigraph(G) knowing or assuming that
        Edges(G) 'subseteq' (Vertices(G) x Vertices(G)).
        '''
        from . import is_digraph_folding
        _G_sub = self.graph
        return is_digraph_folding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def derive_size_in_natural(self, **defaults_config):
        '''
        From self = IsDigraph(G), derive ||G|| in Natural, i.e.
        derive the fact that the size of G (the number of edges in G)
        is a Natural number. This method is called as a side-effect,
        and depends on the fact that a digraph is also a graph.
        '''
        from proveit.graphs import graph_size_in_natural
        _G_sub = self.element
        return graph_size_in_natural.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def derive_is_graph(self, **defaults_config):
        '''
        From self = IsDigraph(G), derive IsGraph(G), i.e. derive the
        fact that G is also a graph more generally.
        '''
        from .import digraph_is_graph
        _G_sub = self.element
        return digraph_is_graph.instantiate(
                {G:_G_sub}, auto_simplify=False)
