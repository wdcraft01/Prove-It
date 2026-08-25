from proveit import e, w, G, E, V, equality_prover, prover
from proveit.logic import (
        Forall, Functions, InSet, SetMembership, SetNonmembership)
from proveit.graphs import Edges, Graph


class EdgeWeightFxnsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    EdgeWeightFxns(G) of possible edge-weighting functions on graph G.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From self = [w in EdgeWeightFxns(G)],
        deduce and return the equality:
            [w in EdgeWeightFxns(G)] = [w in Functions(Edges(G), Real)]
        '''
        from . import edge_weight_fxns_membership_def
        element = self.element
        _G_sub  = self.domain.operand
        return edge_weight_fxns_membership_def.instantiate(
                {G:_G_sub, w:element},auto_simplify=False)

    def as_defined(self):
        '''
        From self = [w in EdgeWeightFxns(G)], return
        [w in Functions(Edges(G), Real)]
        (i.e., an expression (not a judgment) about w being in the
        set of functions from Edges(G) to the Real numbers).
        '''
        from proveit.numbers import Real
        _w = self.element
        _G = self.domain.operand
        return InSet(_w, Functions(Edges(_G), Real))

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [w in EdgeWeightFxns(G)],
        derive and return [w(e) in RealNonNeg for all e in Edges(G)],
        knowing or assuming self.
        '''
        from . import edge_weight_fxns_membership_unfolding
        _G_sub = self.domain.operand
        element = self.element
        return edge_weight_fxns_membership_unfolding.instantiate(
            {G:_G_sub, w:element}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [elem in EdgeWeightFxns(G)], and
        knowing or assuming [elem in Functions(Edges(G), Real)],
        derive and return self.
        '''
        from . import edge_weight_fxns_membership_folding
        _w_sub = self.element
        _G_sub  = self.domain.operand
        return edge_weight_fxns_membership_folding.instantiate(
            {w:_w_sub, G:_G_sub}, auto_simplify=False)


# leaving the remainder content (copied from edges_membership.py)
# here as temp placeholder for future development

# class EdgesNonmembership(SetNonmembership):
#     '''
#     Defines methods that apply to non-membership in the set
#     Edges(G(V,E)) of the edges E of graph G.
#     '''

#     def __init__(self, element, domain):
#         SetNonmembership.__init__(self, element, domain)

#     def side_effects(self, judgment):
#         '''
#         Currently no side-effects for EdgesNonmembership.
#         '''
#         return
#         yield

#     @equality_prover('defined', 'define')
#     def definition(self, **defaults_config):
#         '''
#         From self = [elem not in Edges(Graph(V,E))], deduce and
#         return: [elem not in Edges(Graph(V,E))] = [elem not in E].
#         '''

#         from . import edges_nonmembership_def
#         element = self.element
#         _V_sub  = self.domain.graph.vertex_set
#         _E_sub  = self.domain.graph.edge_set
#         return edges_nonmembership_def.instantiate(
#                 {e:element, V:_V_sub, E:_E_sub },auto_simplify=False)

#     def as_defined(self):
#         '''
#         From self = [elem not in Edges(Graph(V,E))],
#         return: [elem not in E] (i.e. an expression, not a Judgment)
#         '''
#         if isinstance(self.domain.operand, Graph):
#             from proveit.logic import NotInSet
#             element = self.element
#             _E = self.domain.graph.edge_set
#             return NotInSet(element, _E)
#         else:
#             raise NotImplementedError(
#                 "EdgesNonmembership.as_defined() was called on "
#                 f"self = {self.expr} with domain = {self.expr.domain}, "
#                 "but the method is implemented only for domains of the "
#                 "form Edges(G) where G is an explicit Graph object "
#                 "of the form G = Graph(V,E) with a named edge set E.")

#     @prover
#     def unfold(self, **defaults_config):
#         '''
#         From self = [elem not in Edges(Graph(V,E))],
#         derive and return [elem not in E], knowing or assuming self,
#         (and that E is a subset of [V]^2, i.e., a subset of the set
#         of 2-element subsets of V).
#         '''
#         from . import edges_nonmembership_unfolding
#         element = self.element
#         _V_sub  = self.domain.graph.vertex_set
#         _E_sub  = self.domain.graph.edge_set
#         return edges_nonmembership_unfolding.instantiate(
#             {e:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

#     @prover
#     def conclude(self, **defaults_config):
#         '''
#         Called on self = [elem not in Edges(Graph(V,E))], and
#         knowing or assuming [elem not in E] (and that E is a subset
#         of [V]^2, a subset of the set of 2-element subsets of V)
#         derive and return self.
#         '''
#         from . import edges_nonmembership_folding
#         element = self.element
#         _V_sub  = self.domain.graph.vertex_set
#         _E_sub  = self.domain.graph.edge_set
#         return edges_nonmembership_folding.instantiate(
#             {e:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

