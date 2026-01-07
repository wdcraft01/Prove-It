from proveit import v, E, G, H, V, equality_prover, prover
from proveit.logic import (
        And, Equals, Forall, InSet, SetMembership, SetNonmembership)
from proveit.numbers import IntegerEven
from proveit.graphs import Degree, Graph, Subgraph, Vertices


class CycleSpaceMembership(SetMembership):
    '''
    Defines methods that apply to membership in the cycle space
    C(G) of graph G = G(V,E). C(G) consists of the set of all
    even-degree spanning subgraphs of G and constitutes a vector
    space over the 2-element finite field {0, 1}, where vector
    addition is defined by the symmetric difference between the
    edge sets of the subgraphs.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [H in CycleSpace(G))], deduce and return the
        equality:

            [H in CycleSpace(G)] 
             = [H is an even-degree spanning sub-graph of G]
             = [H subgraph G AND Vertices(H)=Vertices(G)
                AND forall v in Vertices(H) (deg(v) is even)]
        '''
        from . import cycle_space_membership_def
        _G_sub = self.domain.operand
        _H_sub = self.element
        return cycle_space_membership_def.instantiate(
                {G:_G_sub, H:_H_sub },auto_simplify=False)

    def as_defined(self):
        '''
        From self = [H in CycleSpace(G)], return the expression:
            [H subgraph G AND Vertices(H)=Vertices(G)
                AND forall v in Vertices(H) (deg(v) is even)]
        (i.e. an expression, not a Judgment).
        '''
        if isinstance(self.domain.operand, Graph):
            from proveit.logic import InSet
            _G_sub = self.domain.operand
            _H_sub = self.element
            _subgraph_stmt = Subgraph(_H_sub, _G_sub)
            _vertices_stmt = Equals(Vertices(_H_sub), Vertices(_G_sub))
            _even_stmt = Forall(v, InSet(Degree(v, _H_sub), IntegerEven),
                                domain=Vertices(_H_sub))
            return And(_subgraph_stmt, _vertices_stmt, _even_stmt)
        else:
            raise NotImplementedError(
                "CycleSpaceMembership.as_defined() was called on "
                f"self = {self.expr} with domain = {self.expr.domain}, "
                "but the method is implemented only for domains of the "
                "form CycleSpace(G) where G is known or assumed to be "
                "an element of Graphs.")

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [H in CycleSpace(G)], derive and return:

            [H subgraph G AND Vertices(H)=Vertices(G)
                AND forall v in Vertices(H) (deg(v) is even)],

        knowing or assuming self.
        '''
        from . import cycle_space_membership_unfolding
        _G_sub = self.domain.operand
        _H_sub = self.element
        return cycle_space_membership_unfolding.instantiate(
            {G:_G_sub, H:_H_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [H in CycleSpace(G)], and knowing or
        assuming that:

            * G in Graphs;
            * H subgraph G;
            * Vertices(H) = Vertices(G);
            * and forall v in Vertices(H) [v is even],

        derive and return self.
        '''
        from . import cycle_space_membership_folding
        _G_sub = self.domain.operand
        _H_sub = self.element
        return cycle_space_membership_folding.instantiate(
            {G:_G_sub, H:_H_sub}, auto_simplify=False)


# AND leaving all of this here as a placeholder as well.
class CycleSpaceNonmembership(SetNonmembership):
    '''
    Defines methods that apply to non-membership in the cycle space
    C(G) of graph G = G(V,E). G(C) consists of the set of all
    even-degree subgraphs of $G$ and constitutes a vector space
    over the 2-element finite field {0, 1}, where vector addition
    is defined by the symmetric difference between the edge sets of
    the subgraphs.
    '''

    def __init__(self, element, domain):
        SetNonmembership.__init__(self, element, domain)

#     def side_effects(self, judgment):
#         '''
#         Currently no side-effects for VerticesNonmembership.
#         '''
#         return
#         yield

#     @equality_prover('defined', 'define')
#     def definition(self, **defaults_config):
#         '''
#         From self = [elem not in Vertices(Graph(V,E))], deduce and
#         return: [elem not in Vertices(Graph(V,E))] = [elem not in V].
#         '''

#         from . import vertices_nonmembership_def
#         element = self.element
#         _V_sub  = self.domain.graph.vertex_set
#         _E_sub  = self.domain.graph.edge_set
#         return vertices_nonmembership_def.instantiate(
#                 {v:element, V:_V_sub, E:_E_sub },auto_simplify=False)

#     def as_defined(self):
#         '''
#         From self = [elem not in Vertices(Graph(V,E))],
#         return: [elem not in V] (i.e. an expression, not a Judgment)
#         '''
#         if isinstance(self.domain.operand, Graph):
#             from proveit.logic import NotInSet
#             element = self.element
#             _V =  self.domain.graph.vertex_set
#             return NotInSet(element, _V)
#         else:
#             raise NotImplementedError(
#                 "VerticesNonmembership.as_defined() called on "
#                 f"self = {self.expr} with domain = {self.expr.domain}, "
#                 "but the method is implemented only for domains of the "
#                 "form Vertices(G) where G is an explicit Graph object "
#                 "of the form G = Graph(V,E) with a named vertex set V.")

#     @prover
#     def unfold(self, **defaults_config):
#         '''
#         From self = [elem not in Vertices(Graph(V,E))],
#         derive and return [elem not in V], knowing or assuming self,
#         (and that E is a subset of [V]^2, i.e., a subset of the set
#         of 2-element subsets of V).
#         '''
#         from . import vertices_nonmembership_unfolding
#         element = self.element
#         _V_sub  = self.domain.graph.vertex_set
#         _E_sub  = self.domain.graph.edge_set
#         return vertices_nonmembership_unfolding.instantiate(
#             {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

#     @prover
#     def conclude(self, **defaults_config):
#         '''
#         Called on self = [elem not in Vertices(Graph(V,E))], and
#         knowing or assuming [elem not in V] (and that E is a subset
#         of [V]^2, a subset of the set of 2-element subsets of V)
#         derive and return self.
#         '''
#         from . import vertices_nonmembership_folding
#         element = self.element
#         _V_sub  = self.domain.graph.vertex_set
#         _E_sub  = self.domain.graph.edge_set
#         return vertices_nonmembership_folding.instantiate(
#             {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

