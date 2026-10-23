from proveit import G, Function, Literal
from proveit import equality_prover, prover, ClassMembership
from proveit import f, A, B

class IsUndirectedGraph(ClassMembership):
    '''
    IsUndirectedGraph(G) is the class predicate claim that G is an
    undirected graph, and replaces the problematic conceptual approach
    of claiming that "G is in the class of undirected graphs". For our
    purposes here, the class of undirected graphs will be understood to
    consist of finite simple graphs of the form (V,E), consisting of
    vertex set V and edge set E ("simple" here means no loops and no
    parallel edges). Some textbooks insist that V be non-empty, but
    until we run into problems, we will allow V to be empty (producing
    the "empty undirected graph" G(EmptySet, EmptySet)).
    The claim IsUndirectedGraph(G) then is tantamount to claiming that
    G is an ordered pair (V, E) of vertices V and edges E such that
    E is a subset of [V]^2 (the set of 2-element subsets of V).
    '''
    _operator_ = Literal('IsUndirectedGraph',
                         r'\textrm{IsUndirectedGraph}',
                         theory=__file__)
    
    def __init__(self, G, *, styles=None):
        ClassMembership.__init__(self, IsUndirectedGraph._operator_,
                                 G, styles=styles)
        self.graph = G

    def formatted_class(self, format_type):
        if format_type == 'latex':
            return r'{\textrm{UndirectedGraphs}}'
        return r'UndirectedGraphs'

    def side_effects(self, judgment):
        '''
        Yield side-effects when proving or assuming
        'UnidirectedGraphs(G)':

            * IsGraph(G);
            * ||G|| in Natural (this assumes that G is finite);
            * Edges(G) 'subseteq' [Vertices(G)]^2
        '''
        yield self.derive_is_graph
        yield self.derive_size_in_natural
        yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Derive and return that

            IsUndirectedGraph(G) =
            Edges(G) 'subseteq' [Vertices(G)]^2

        i.e., that G being an undirected graph means that its edges
        consist of a subset of the set of 2-element subsets of the
        set of vertices.
        '''
        from . import is_undirected_graph_def
        _G_sub = self.graph
        return is_undirected_graph_def.instantiate(
                {G: _G_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From self=IsUndirectedGraph(G), return the expression (not
        a Judgment):
            Edges(G) 'subseteq' [Vertices(G)]^2
        i.e., that G being an undirected graph means that its edges
        consist of a subset of the set of 2-element subsets of the
        set of vertices.
        '''
        from proveit.logic.sets import KPowerSet, SubsetEq
        from proveit.numbers import two
        from proveit.graphs import Edges, Vertices
        _G_sub = self.graph
        return SubsetEq(Edges(_G_sub), KPowerSet(Vertices(_G_sub), two))

    @prover
    def unfold(self, **defaults_config):
        '''
        From IsUndirectedGraph(G), derive and return:

            |- Edges(G) 'subseteq' [Vertices(G)]^2

        i.e., that the edges of undirected graph G consist of a subset
        of the two-element subsets of the set of vertices.
        '''
        from . import is_undirected_graph_unfolding
        _G_sub = self.graph
        return is_undirected_graph_unfolding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Prove self = IsUndirectedGraph(G) knowing or assuming that
        Edges(G) 'subseteq' [Vertices(G)]^2.
        '''
        from . import is_undirected_graph_folding
        _G_sub = self.graph
        return is_undirected_graph_folding.instantiate(
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
        From self = IsUndirectedGraph(G), derive IsGraph(G), i.e.
        derive the fact that G is also a graph more generally.
        '''
        from .import undirected_graph_is_graph
        _G_sub = self.element
        return undirected_graph_is_graph.instantiate(
                {G:_G_sub}, auto_simplify=False)
