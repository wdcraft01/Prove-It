from proveit import e, m, n, v, x, y, E, G, V, equality_prover, prover
from proveit.logic import ClassMembership, SetMembership, SetNonmembership
from proveit.graphs import Graph


class SquareGridPointsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of 
    square grid points, SquareGridPoints(m, n).
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [v in SquareGridPoints(m, n)], deduce and return
        the equality:
        self = [v in {(x,y)|x <= n, y <= m}_(x,y in NaturalPos)].
        '''
        from . import square_grid_points_membership_def
        element = self.element
        _m_sub  = self.domain.operands[0]
        _n_sub  = self.domain.operands[1]
        return square_grid_points_membership_def.instantiate(
                {v:element, m:_m_sub, n:_n_sub}, auto_simplify=False)

    def as_defined(self, **defaults_config):
        '''
        From self = [v in SquareGridPoints(m, n)], return the
        expression: [v in {(x,y)|x <= n, y <= m}_(x,y in NaturalPos)]
        (i.e., an _expression_, not a judgment).
        '''
        from proveit import ExprTuple
        from proveit.logic import InSet, SetOfAll
        from proveit.numbers import LessEq, NaturalPos
        element = self.element
        _set_of_all = SetOfAll((x,y), ExprTuple(x, y),
                      conditions=[LessEq(x, n), LessEq(y, m)],
                      domain=NaturalPos)
        return InSet(element, _set_of_all)

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [v in SquareGridPoints(m, n)], derive and
        return that: [v in {(x,y)|x <= n, y <= m}_(x,y in NaturalPos)],
        knowing or assuming self.
        '''
        from . import square_grid_points_membership_unfolding
        element = self.element
        _m_sub  = self.domain.operands[0]
        _n_sub  = self.domain.operands[1]
        return square_grid_points_membership_unfolding.instantiate(
                {v:element, m:_m_sub, n:_n_sub})

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [v in SquareGridPoints(m, n)],
        and knowing or assuming that
        [v in {(x,y)|x <= n, y <= m}_(x,y in NaturalPos)] (along with
        m,n in NaturalPos), derive and return self.
        '''
        from . import square_grid_points_membership_folding
        element = self.element
        _m_sub  = self.domain.operands[0]
        _n_sub  = self.domain.operands[1]
        return square_grid_points_membership_folding.instantiate(
                {v:element, m:_m_sub, n:_n_sub})


class SquareGridEdgesMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of 
    square grid edges, SquareGridEdges(m, n), the set of edges
    in an m x n square grid.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [v in SquareGridEdges(m, n)], deduce and return
        the equality:
        self = [v in {{x,y}|dist(x, y) = 1}_
                     (x,y in SquareGridPoints(m,n))].
        '''
        from . import square_grid_edges_membership_def
        element = self.element
        _m_sub  = self.domain.operands[0]
        _n_sub  = self.domain.operands[1]
        return square_grid_edges_membership_def.instantiate(
                {e:element, m:_m_sub, n:_n_sub}, auto_simplify=False)

    def as_defined(self, **defaults_config):
        '''
        From self = [v in SquareGridEdges(m, n)], return the
        expression: [v in {{x,y}|dist(x, y) = 1}_
                     (x,y in SquareGridPoints(m,n))]
        (i.e., an _expression_, not a judgment).
        '''
        from proveit import ExprTuple
        from proveit.logic import Equals, InSet, Set, SetOfAll
        from proveit.numbers import one, NaturalPos
        from proveit.linear_algebra import EuclideanDistance
        from proveit.graphs import SquareGridPoints
        element = self.element
        _set_of_all = SetOfAll((x,y), Set(x, y),
                      conditions=[Equals(EuclideanDistance(x, y), one)],
                      domain=SquareGridPoints(m, n))
        return InSet(element, _set_of_all)

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [v in SquareGridEdges(m, n)], derive and
        return that: [v in {{x,y}|dist(x, y) = 1}_
                     (x,y in SquareGridPoints(m,n))],
        knowing or assuming self.
        '''
        from . import square_grid_edges_membership_unfolding
        element = self.element
        _m_sub  = self.domain.operands[0]
        _n_sub  = self.domain.operands[1]
        return square_grid_edges_membership_unfolding.instantiate(
                {e:element, m:_m_sub, n:_n_sub})

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [v in SquareGridEdges(m, n)],
        and knowing or assuming that
        [v in {{x,y}|dist(x, y) = 1}_(x,y in SquareGridPoints(m,n))]
        (along with m,n in NaturalPos), derive and return self.
        '''
        from . import square_grid_edges_membership_folding
        element = self.element
        _m_sub  = self.domain.operands[0]
        _n_sub  = self.domain.operands[1]
        return square_grid_edges_membership_folding.instantiate(
                {e:element, m:_m_sub, n:_n_sub})


class SquareGridSubgraphsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    subgraphs of a square grid graph SquareGridGraph(m, n)
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        """
        From self = [G in SquareGridSubgraphs(m,n)], deduce and
        return that: [G is subgraph of SquareGridGraph(m,n)]
        """
        return
        # from . import vertices_membership_def
        # element = self.element
        # _V_sub  = self.domain.graph.vertex_set
        # _E_sub  = self.domain.graph.edge_set
        # return vertices_membership_def.instantiate(
        #         {v:element, V:_V_sub, E:_E_sub },auto_simplify=False)

    def as_defined(self):
        '''
        From self = [G in SquareGridSubgraphs(m,n)], return:
        [G in SquareGridSubgraphs(m,n)]
        = [G is subgraph of SquareGridGraph(m,n)]
        (i.e., an equality expression, not a Judgment).
        '''
        return
        # if isinstance(self.domain.operand, Graph):
        #     from proveit.logic import InSet
        #     element = self.element
        #     _V =  self.domain.graph.vertex_set
        #     return InSet(element, _V)
        # else:
        #     raise NotImplementedError(
        #         "VerticesMembership.as_defined() was called on "
        #         f"self = {self.expr} with domain = {self.expr.domain}, "
        #         "but the method is implemented only for domains of the "
        #         "form Vertices(G) where G is an explicit Graph object "
        #         "of the form G = Graph(V,E) with a named vertex set V.")

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [G in SquareGridSubgraphs(m,n)], derive and
        return that: [G is subgraph of SquareGridGraph(m,n)],
        knowing or assuming self.
        '''
        return
        # from . import vertices_membership_unfolding
        # element = self.element
        # _V_sub  = self.domain.graph.vertex_set
        # _E_sub  = self.domain.graph.edge_set
        # return vertices_membership_unfolding.instantiate(
        #     {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [G in H], where H = SquareGridSubgraphs(m,n),
        and knowing or assuming that [Vertices(G) subset Vertices(H)]
        and [Edges(V) subset Edges(H)], derive and return self.
        '''
        return
        # from . import vertices_membership_folding
        # element = self.element
        # _V_sub  = self.domain.graph.vertex_set
        # _E_sub  = self.domain.graph.edge_set
        # return vertices_membership_folding.instantiate(
        #     {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)


class GridGraphsMembership(ClassMembership):
    '''
    Defines methods that apply to membership in the class of all
    GridGraphs, a special sub-class of Graphs.
    '''

    def __init__(self, element, domain):
        ClassMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        """
        From self = [G in GridGraphs], deduce and return that:
            [G in GridGraphs] =
            [G in Graphs]
            AND [forall (x,y) in Vertices(G), x,y in Integer]
            AND [forall {(x1, y1), (x2, y2)} in Edges(G),
                    [(x1=x2) AND (|y1-y2|=1)] 
                    OR  [|x1-x2|=1 AND (y1=y2)]]
        """

        from . import vertices_membership_def
        element = self.element
        _V_sub  = self.domain.graph.vertex_set
        _E_sub  = self.domain.graph.edge_set
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
            _V =  self.domain.graph.vertex_set
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
        _V_sub  = self.domain.graph.vertex_set
        _E_sub  = self.domain.graph.edge_set
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
        _V_sub  = self.domain.graph.vertex_set
        _E_sub  = self.domain.graph.edge_set
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
        _V_sub  = self.domain.graph.vertex_set
        _E_sub  = self.domain.graph.edge_set
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
            _V =  self.domain.graph.vertex_set
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
        _V_sub  = self.domain.graph.vertex_set
        _E_sub  = self.domain.graph.edge_set
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
        _V_sub  = self.domain.graph.vertex_set
        _E_sub  = self.domain.graph.edge_set
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
