from proveit import v, E, G, V, equality_prover, prover
from proveit.logic import SetMembership, SetNonmembership
from proveit.graphs import Graph


class VerticesMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    Vertices(G(V,E)) of the vertices V of graph G.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [elem in Vertices(Graph(V,E))], deduce and return:
            [elem in Vertices(Graph(V,E))] = [elem in V]
        '''

        from . import vertices_membership_def
        element = self.element
        _V_sub  = self.domain.graph.vertices
        _E_sub  = self.domain.graph.edges
        return vertices_membership_def.instantiate(
                {v:element, V:_V_sub, E:_E_sub },auto_simplify=False)

    def as_defined(self):
        '''
        From self = [elem in Vertices(Graph(V,E))], return: [elem in V]
        (i.e. an expression, not a Judgment). Only works if the
        Vertices domain has as an operand an actual Graph object
        Graph(V,E) with a specified vertex set V.
        '''
        if isinstance(self.domain.operand, Graph):
            from proveit.logic import InSet
            element = self.element
            _V =  self.domain.graph.vertices
            return InSet(element, _V)
        else:
            raise NotImplementedError(
                "VerticesMembership.as_defined() was called on "
                f"self = {self.expr} with domain = {self.expr.domain}, "
                "but the method is implemented only for domains of the "
                "form Vertices(G) where G is an explicit Graph object "
                "of the form G = Graph(V,E) with a named vertex set V.")

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [elem in Vertices(Graph(V,E))],
        derive and return [elem in V], knowing or assuming self.
        '''
        from . import vertices_membership_unfolding
        element = self.element
        _V_sub  = self.domain.graph.vertices
        _E_sub  = self.domain.graph.edges
        return vertices_membership_unfolding.instantiate(
            {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [elem in Vertices(Graph(V,E))], and
        knowing or assuming [elem in V] (and that E is a subset
        of [V]^2, a subset of the set of 2-element subsets of V)
        derive and return self.
        '''
        from . import vertices_membership_folding
        element = self.element
        _V_sub  = self.domain.graph.vertices
        _E_sub  = self.domain.graph.edges
        return vertices_membership_folding.instantiate(
            {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)


class VerticesNonmembership(SetNonmembership):
    '''
    Defines methods that apply to non-membership in the set
    Vertices(G(V,E)) of the vertices V of graph G.
    '''

    def __init__(self, element, domain):
        SetNonmembership.__init__(self, element, domain)

    def side_effects(self, judgment):
        '''
        Currently no side-effects for VerticesNonmembership.
        '''
        return
        yield

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [elem not in Vertices(Graph(V,E))], deduce and
        return: [elem not in Vertices(Graph(V,E))] = [elem not in V].
        '''

        from . import vertices_nonmembership_def
        element = self.element
        _V_sub  = self.domain.graph.vertices
        _E_sub  = self.domain.graph.edges
        return vertices_nonmembership_def.instantiate(
                {v:element, V:_V_sub, E:_E_sub },auto_simplify=False)

    def as_defined(self):
        '''
        From self = [elem not in Vertices(Graph(V,E))],
        return: [elem not in V] (i.e. an expression, not a Judgment)
        '''
        if isinstance(self.domain.operand, Graph):
            from proveit.logic import NotInSet
            element = self.element
            _V =  self.domain.graph.vertices
            return NotInSet(element, _V)
        else:
            raise NotImplementedError(
                "VerticesNonmembership.as_defined() called on "
                f"self = {self.expr} with domain = {self.expr.domain}, "
                "but the method is implemented only for domains of the "
                "form Vertices(G) where G is an explicit Graph object "
                "of the form G = Graph(V,E) with a named vertex set V.")

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [elem not in Vertices(Graph(V,E))],
        derive and return [elem not in V], knowing or assuming self,
        (and that E is a subset of [V]^2, i.e., a subset of the set
        of 2-element subsets of V).
        '''
        from . import vertices_nonmembership_unfolding
        element = self.element
        _V_sub  = self.domain.graph.vertices
        _E_sub  = self.domain.graph.edges
        return vertices_nonmembership_unfolding.instantiate(
            {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [elem not in Vertices(Graph(V,E))], and
        knowing or assuming [elem not in V] (and that E is a subset
        of [V]^2, a subset of the set of 2-element subsets of V)
        derive and return self.
        '''
        from . import vertices_nonmembership_folding
        element = self.element
        _V_sub  = self.domain.graph.vertices
        _E_sub  = self.domain.graph.edges
        return vertices_nonmembership_folding.instantiate(
            {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)


class OddVerticesMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    OddVertices(G) of the odd-degree vertices of graph G.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [elem in OddVertices(G)], deduce and return:
        [elem in OddVertices(G)]
         = [elem in {x, Degree(x, G) in IntegerOdd}_{x in Vertices(G)}]
        '''

        from . import odd_vertices_membership_def
        element = self.element
        _G_sub = self.domain.graph
        return odd_vertices_membership_def.instantiate(
                {v:element, G:_G_sub },auto_simplify=False)

    def as_defined(self):
        '''
        From self = [elem in OddVertices(G)], return:
        [elem in {x, Degree(x, G) in IntegerOdd}_{x in Vertices(G)}]
        (i.e. an expression, not a Judgment).
        '''
        from proveit import x
        from proveit.logic import InSet, SetOfAll
        from proveit.numbers import IntegerOdd
        from proveit.graphs import Degree, Vertices
        element = self.element
        _G = self.domain.graph
        return InSet(element, SetOfAll(x, x,
                       conditions=[InSet(Degree(x, G), IntegerOdd)],
                       domain=Vertices(_G)))

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [elem in OddVertices(G)], derive and return:
        [elem in {x, Degree(x, G) in IntegerOdd}_{x in Vertices(G)}],
        knowing or assuming self and knowing or assuming that G is
        in the class of Graphs.
        '''
        from . import odd_vertices_membership_unfolding
        element = self.element
        _G_sub  = self.domain.graph
        return odd_vertices_membership_unfolding.instantiate(
            {v:element, G:_G_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [elem in OddVertices(G)], and knowing or
        assuming that:
        [elem in {x, Degree(x, G) in IntegerOdd}_{x in Vertices(G)}],
        along with knowing or assuming that G is in the class of Graphs,
        derive and return self.
        '''
        from . import odd_vertices_membership_folding
        element = self.element
        _G_sub  = self.domain.graph
        return odd_vertices_membership_folding.instantiate(
            {v:element, G:_G_sub}, auto_simplify=False)
