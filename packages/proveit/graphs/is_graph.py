from proveit import G, Function, Literal
from proveit import equality_prover, prover, ClassMembership
from proveit import f, A, B

class IsGraph(ClassMembership):
    '''
    IsGraph(G) is the class predicate claim that G is a graph, and
    replaces the problematic conceptual approach of claiming that
    "G is in the class of Graphs".
    For our purposes here, the class of graphs will be understood to
    consist of finite simple graphs of the form (V,E), consisting of
    vertex set V and edge set E ("simple" here means no loops and no
    parallel edges). Some textbooks insist that V be non-empty, but
    until we run into problems, we will allow V to be empty (producing
    the "empty graph" G(EmptySet, EmptySet)).
    The claim IsGraph(G) then is tantamount to claiming that G is
    an ordered pair (V, E) of vertices V and edges E such that
    E is a subset of the set of 2-element subsets of V.
    '''
    _operator_ = Literal('IsGraph', r'\textrm{IsGraph}',
                         theory=__file__)
    
    def __init__(self, G, *, styles=None):
        ClassMembership.__init__(self, IsGraph._operator_,
                                 G, styles=styles)
        self.graph = G

    def formatted_class(self, format_type):
        if format_type == 'latex':
            return r'{\textrm{Graphs}}'
        return r'Graphs'

    def side_effects(self, judgment):
        '''
        Yield side-effects when proving or assuming 'IsGraph(G)':
            * ||G|| in Natural (this assumes that G is finite)
            * Edges(G) 'subseteq' [Vertices(G)]^{2}
        '''
        yield self.derive_size_in_natural
        yield self.unfold

    @prover
    def conclude(self, **defaults_config):
        '''
        Prove self IsGraph(G) knowing or assuming that
        Edges(G) 'subseteq' [Vertices(G)]^2.
        '''
        from . import is_graph_folding
        _G_sub = self.graph
        return is_graph_folding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Derive and return that

            IsGraph(G) = Edges(G) 'subseteq' [Vertices(G)]^2

        i.e., that G being a graph means that its edges consist of
        a subset of the set of 2-element subsets of its vertices.
        '''
        from . import is_graph_def
        _G_sub = self.graph
        return is_graph_def.instantiate({G: _G_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From self=IsGraph(G), return the expression (not a Judgment):
            Edges(G) 'subseteq' [Vertices(G)]^2
        i.e., that G being a graph means that its edges consist of
        a subset of the set of 2-element subsets of its vertices.
        From self=IsSurjection(f, A, B), return
        IsFunction(f, A, B) and Image(f, A) = B
        '''
        from proveit.logic.sets import KPowerSet, SubsetEq
        from proveit.numbers import two
        from proveit.graphs import Edges, Vertices
        _G = self.graph
        return SubsetEq(Edges(_G), KPowerSet(Vertices(G), two))

    @prover
    def unfold(self, **defaults_config):
        '''
        From IsGraph(G), derive and return:

            |- Edges(G) 'subseteq' [Vertices(G)]^2

        i.e., that the edges of G consist of a subset of of the set
        of 2-element subsets of the vertices of G.
        '''
        from . import is_graph_unfolding
        _G_sub = self.graph
        return is_graph_unfolding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def derive_size_in_natural(self, **defaults_config):
        '''
        From self = IsGraph(G), derive ||G|| in Natural, i.e. derive the
        fact that the size of G (the number of edges in G) is a
        Natural number. Called as a side-effect.
        '''
        from . import graph_size_in_natural
        _G = self.element
        return graph_size_in_natural.instantiate(
                {G:_G}, auto_simplify=False)
