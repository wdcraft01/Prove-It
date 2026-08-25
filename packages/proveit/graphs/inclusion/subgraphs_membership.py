from proveit import v, E, V, equality_prover, prover
from proveit.logic import SetMembership, SetNonmembership
from proveit.graphs import Graph


class SubgraphsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of subgraphs
    of a graph G. A subgraph H of a graph G is itself a graph, with
    vertex set V(H) and edge set E(H). A graph H is called a subgraph
    of G (written H subset_eq G with the usual subset_eq symbol), if:

        V(H) subset_eq V(G) AND E(H) subset_eq E(G)

    (with the additional provision that any vertex appearing as an
    endpoint in E(H) must then also appear in V(H)).
    Most simply, H in Subgraphs(G) = H Subgraph G.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    # placeholder for future work
    # @equality_prover('defined', 'define')
    # def definition(self, **defaults_config):
    #     '''
    #     From self = [elem in CycleSpace(Graph(V,E))], deduce and return:
    #         [elem in Vertices(Graph(V,E))] 
    #          = [elem is a even-degree sub-graph of G]
    #     '''

    #     from . import vertices_membership_def
    #     element = self.element
    #     _V_sub  = self.domain.graph.vertex_set
    #     _E_sub  = self.domain.graph.edge_set
    #     return vertices_membership_def.instantiate(
    #             {v:element, V:_V_sub, E:_E_sub },auto_simplify=False)

    # placeholder for future work
    # def as_defined(self):
    #     '''
    #     From self = [elem in CycleSpace(Graph(V,E))], return:
    #         [elem is an even-degree subgraph of G]
    #     (i.e. an expression, not a Judgment).
    #     '''
    #     if isinstance(self.domain.operand, Graph):
    #         from proveit.logic import InSet
    #         element = self.element
    #         _V =  self.domain.graph.vertex_set
    #         return InSet(element, _V)
    #     else:
    #         raise NotImplementedError(
    #             "VerticesMembership.as_defined() was called on "
    #             f"self = {self.expr} with domain = {self.expr.domain}, "
    #             "but the method is implemented only for domains of the "
    #             "form Vertices(G) where G is an explicit Graph object "
    #             "of the form G = Graph(V,E) with a named vertex set V.")

    # placeholder for future work
    # @prover
    # def unfold(self, **defaults_config):
    #     '''
    #     From self = [elem in Vertices(Graph(V,E))],
    #     derive and return [elem in V], knowing or assuming self.
    #     '''
    #     from . import vertices_membership_unfolding
    #     element = self.element
    #     _V_sub  = self.domain.graph.vertex_set
    #     _E_sub  = self.domain.graph.edge_set
    #     return vertices_membership_unfolding.instantiate(
    #         {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)

    # placeholder for future work
    # @prover
    # def conclude(self, **defaults_config):
    #     '''
    #     Called on self = [elem in Vertices(Graph(V,E))], and
    #     knowing or assuming [elem in V] (and that E is a subset
    #     of [V]^2, a subset of the set of 2-element subsets of V)
    #     derive and return self.
    #     '''
    #     from . import vertices_membership_folding
    #     element = self.element
    #     _V_sub  = self.domain.graph.vertex_set
    #     _E_sub  = self.domain.graph.edge_set
    #     return vertices_membership_folding.instantiate(
    #         {v:element, V:_V_sub, E:_E_sub}, auto_simplify=False)



# AND leaving all of this here as a placeholder as well.
class SubgraphsNonmembership(SetNonmembership):
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

