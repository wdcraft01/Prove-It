from proveit import equality_prover, Function, Literal, prover
from proveit import e, w, E, G, V
from proveit.logic import ClassMembership
# from proveit.graphs import 

class GraphsMembership(ClassMembership):
    '''
    Defines methods that apply to membership in the class of Graphs
    (see Graphs class in graphs/graph.py), consisting of simple
    graphs of the (conceptual) form (V, E), where V is the a set of
    vertices and E is a set of edges such that E is subset of [V]^2
    (i.e. E is a subset of the set of two-element subsets of the
    vertices V).
    Graphs membership is a little copmlicated because we allow for
    possibilities such as an abstract G to be in Graphs, but also for
    the possibility of a specified tuple Graph(V, E) to be in Graphs.
    '''

    def __init__(self, element, domain):
        from . import Graphs
        ClassMembership.__init__(self, element, domain)
        if domain != Graphs:
            raise TypeError("domain expected to be Graphs, not %s"
                            %domain.__class__)

    def side_effects(self, judgment):
        '''
        Yield side-effects when proving or assuming 'G in Graphs',
        the main side-effect being that ||G|| in Natural.
        This needs updated, since Graphs includes infinite graphs,
        and in at least some such cases it is not clear that the 
        order is still in Naturals.
        '''
        yield self.derive_size_in_natural

    @equality_prover('existential_defined', 'existential_define')
    def existential_definition(self, **defaults_config):
        '''
        From [G in Graphs], where G might be abstract and not (yet)
        specified as an explicit Graph(V, E) with explicit vertex set
        V and explicit edge set E, deduce and return the equality:
            [G in Graphs]
            = Exists_{(V,E)|E subseteq [V]^2}(G = Graph(V,E)).
        '''
        from .import g_in_graphs_existential_def
        element = self.element
        return g_in_graphs_existential_def.instantiate(
                {G:element}, auto_simplify=False)

    def as_defined_existentially(self):
        '''
        From [G in Graphs], where G might be abstract and not (yet)
        specified as an explicit Graph(V, E) with explicit vertex set
        V and explicit edge set E, return the expression (NOT a
        judgment):
            Exists_{(V,E)|E subseteq [V]^2}(G = Graph(V,E)).
        '''
        from proveit.logic import Exists, Equals
        from proveit.logic.sets import KPowerSet, SubsetEq
        from proveit.numbers import two
        from proveit.graphs import Graph
        element = self.element
        return Exists((V, E), Equals(element, Graph(V, E)),
                conditions=[SubsetEq(E, KPowerSet(V, two))])

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        If G is of type Graph(V, E) (see Graph() class in graph.py),
        then from [G in Graphs], deduce and return the equality:
        [G in Graphs] = [E subseteq [V]^{2}]
        (i.e., that G in Graphs means that the edges of G are a
        subset of the set of 2-element subsets of the vertices).
        If G is generic without a Graph(V,E) specification, then
        deduce and return the equality:
        [G in Graphs] = [Edges(G) subseteq [Vertices(G)]^{2}].
        Eventually we should be able to combine both cases into the
        second case and use some automatic simplification to take
        Verties(Graph(V,E)) to V and Edges(Graph(V,E)).
        '''
        element = self.element
        from proveit.graphs import Graph
        if isinstance(element, Graph):
            # element looks like Graph(V,E)
            from . import graph_v_e_in_graphs_def
            _V_sub = element.vertices
            _E_sub = element.edges
            return graph_v_e_in_graphs_def.instantiate(
                    {V:_V_sub, E:_E_sub}, auto_simplify=False)
        # else we have a more generic graph element
        from . import g_in_graphs_def
        _G_sub = self.element
        return g_in_graphs_def.instantiate(
                {G:_G_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        If G is of type Graph(V, E) (see Graph() class in graph.py),
        then from [G in Graphs], return the expression (NOT a
        judgment):[E subseteq [V]^{2}]
        (i.e., the edges of G are a subset of the set of 2-element
        subsets of the vertices).
        If G is generic without a Graph(V,E) specification, then
        return the expression (NOT a judgment):
            [Edges(G) subseteq [Vertices(G)]^{2}].
        '''
        element = self.element
        from proveit.logic.sets import KPowerSet, SubsetEq
        from proveit.numbers import two
        from proveit.graphs import Graph
        if isinstance(element, Graph):
            # element looks like Graph(V,E)
            _verts = element.vertices
            _edges = element.edges
            return SubsetEq(_edges, KPowerSet(_verts, two))
        # else we have a more generic graph element
        from proveit.graphs import Edges, Vertices
        return SubsetEq(Edges(element), KPowerSet(Vertices(element), two))

    @prover
    def unfold(self, **defaults_config):
        '''
        If G is of type Graph(V, E) (see Graph class in graph.py),
        then from self = [G in Graphs], derive and return

            [E subseteq [V]^{2}],

        knowing or assuming self.
        If G is generic without a Graph(V,E) specification, then
        derive and return:

            [Edges(G) subseteq [Vertices(G)]^{2}].
        '''
        element = self.element
        from proveit.graphs import Graph
        if isinstance(element, Graph):
            # element looks like Graph(V,E)
            from . import graph_v_e_in_graphs_unfolding
            _V_sub = element.vertices
            _E_sub = element.edges
            return graph_v_e_in_graphs_unfolding.instantiate(
                    {V:_V_sub, E:_E_sub}, auto_simplify=False)
        # else we have a more generic graph element
        from . import g_in_graphs_unfolding
        _G_sub = self.element
        return g_in_graphs_unfolding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        If G is of type Graph(V, E) (see Graph class in graph.py),
        then called on self = [G in Graphs], and knowing or
        assuming that SubsetEq(E, [V]^2), derive and return self.
        If G is generic without a Graph(V,E) specification, then
        called on self = [G in Graphs], and knowing or assuming that
        SubsetEq(Edges(G), [Vertices(G)]^{2}), derive and return self.
        '''
        element = self.element
        from proveit.graphs import Graph
        if isinstance(element, Graph):
            # element looks like Graph(V,E)
            from . import graph_v_e_in_graphs_folding
            _V_sub = element.vertices
            _E_sub = element.edges
            return graph_v_e_in_graphs_folding.instantiate(
                    {V:_V_sub, E:_E_sub}, auto_simplify=False)
        # else we have a more generic graph element
        from . import g_in_graphs_folding
        _G_sub = self.element
        return g_in_graphs_folding.instantiate(
                {G:_G_sub}, auto_simplify=False)

    @prover
    def derive_size_in_natural(self, **defaults_config):
        '''
        From (G in Graphs), derive ||G|| in Natural, i.e. derive the
        fact that the size of G (the number of edges in G) is a
        Natural number. Called as a side-effect.
        '''
        from . import graph_size_in_natural
        _G = self.element
        return graph_size_in_natural.instantiate(
                {G:_G}, auto_simplify=False)

class FiniteGraphsMembership(ClassMembership):

    def __init__(self, element, domain):
        from . import FiniteGraphs
        ClassMembership.__init__(self, element, domain)
        if domain != FiniteGraphs:
            raise TypeError(
                f"Domain expected to be FiniteGraphs, not {domain.__class__}")

    def side_effects(self, judgment):
        '''
        Yield side-effects when proving or assuming 'G in FiniteGraphs',
        the main side-effect being that ||G|| in Natural.
        Should extend this to also have |G| in Natural.
        Should extend this to also have G in Graphs.
        '''
        yield self.derive_size_in_natural

    # def conclude(): see if and when needed

    @prover
    def derive_size_in_natural(self, **defaults_config):
        '''
        From (G in FiniteGraphs), derive ||G|| in Natural, i.e.
        derive the fact that the size of G (the number of edges in G)
        is a Natural number. Called as a side-effect.
        '''
        from . import graph_size_in_natural
        _G = self.element
        return graph_size_in_natural.instantiate(
                {G:_G}, auto_simplify=False)