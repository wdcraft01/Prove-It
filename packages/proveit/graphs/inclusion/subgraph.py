from proveit import (G, H, Function, Literal, Operation, prover,
                     relation_prover, safe_dummy_var)
# from proveit.relation import TransitiveRelation
from .graph_inclusion_relation import GraphInclusionRelation
# from proveit.logic.sets.inclusion.inclusion_relation import InclusionRelation
# from proveit.graphs import Edges, Vertices

class Subgraphs(Function):
    '''
    Given a graph G = G(V, E) with vertex set V and edge set E,
    Subgraphs(G) represents the set of all subgraphs of G (analogous
    to the power set of a set in set theory).
    A subgraph H is itself a graph, with vertex set V(H) and edge set
    E(H). A graph H is called a subgraph of G (written H subset_eq G
    with the usual subset_eq symbol), if:

        V(H) subset_eq V(G) AND E(H) subset_eq E(G)

    (with the additional provision that any vertex appearing as an
    endpoint in E(H) must then also appear in V(H)).
    '''

    # the literal operator of the CycleSpaces operation
    _operator_ = Literal(string_format='Subgraphs',
                         latex_format=r'\mathrm{Subgraphs}',
                         theory=__file__)

    def __init__(self, G, *, styles=None):
        '''
        Given a graph G= G(V,E), represent the set of all possible
        subgraphs of G.
        '''
        self.graph = G
        Function.__init__(
                self, Subgraphs._operator_, G, styles=styles)

    @property
    def is_proper_class(self):
        '''
        The set of subgraphs of a (finite, simple) graph G is itself a
        finite set. This indicates that InSet() should be used instead
        of InClass() when this is a domain.
        '''
        return False

    def membership_object(self, element):
        from .subgraphs_membership import SubgraphsMembership
        return SubgraphsMembership(element, self)

    def nonmembership_object(self, element):
        from .subgraphs_membership import SubgraphsNonmembership
        return SubgraphsNonmembership(element, self)


class Subgraph(GraphInclusionRelation):
    '''
    Subgraph(H, G) represents the claim that graph H is a subgraph of
    graph G, meaning that:

        V(H) subset_eq V(G);
        AND E(H) subset_eq E(G);
        AND that any vertex appearing as an endpoint in E(H)
            must then also appear in V(H).

    Subgraph(H, G) is equivalent to InSet(H, Subgraphs(G)) but uses
    the more common subgraph (subset) notation.
    The Subgraph class has initially been modeled on the SubsetEq()
    class in logic/sets/inclusion, and uses the analogous
    GraphInclusionRelation() class (instead of the set-specific
    InclusionRelation()class).
    '''

    # The operator of the Subgraph operation.
    # Following tradition in graph theory, we use the same operator ⊆
    # for subgraph as we use for subset, relying on the context to
    # distinguish the cases. We modify the string version for clarity.
    _operator_ = Literal(string_format='subgraph',
                         latex_format=r'\subseteq',
                         theory=__file__)

    # map left-hand-sides to Subgraph Judgments
    #   (populated in TransitivityRelation.derive_side_effects)
    known_left_sides = dict()
    # map right-hand-sides to Subgraph Judgments
    #   (populated in TransitivityRelation.derive_side_effects)
    known_right_sides = dict()

    def __init__(self, subgraph, graph, *, styles=None):
        '''
        Create the expression for (H ⊆ G).
        '''
        GraphInclusionRelation.__init__(
                self, Subgraph._operator_, subgraph, graph, styles=styles)

    @staticmethod
    def reversed_operator_str(format_type):
        '''
        Reversing H ⊆ G gives G ⊇ H (subset_eq symbol is changed to
        the supset_eq symbol).
        '''
        return r'\supseteq' if format_type == 'latex' else 'supergraph'

    def remake_constructor(self):
        if self.is_reversed():
            # Use the 'superset_eq' glif if the relation is reversed.
            return 'superset_eq'
        # Use the default.
        return Operation.remake_constructor(self)

    # UNDER DEVELOPMENT
    def _readily_provable(self, *, check_transitive_pair=False):
        '''
        This Subgraph(H, G) relation is readily provable if any of 
        the following hold:
        (a) graphs H and G are provably equal;
        (b) graph H is provably a proper subgraph of G;
        (c) V(H) ⊆ V(G) and E(H) ⊆ E(G) and any vertex appearing as
            an endpt in E(H) also appears in V(H).
        '''
        from proveit.logic import Equals
        if Equals(self.subgraph, self.supergraph).readily_provable():
            return True
        if GraphInclusionRelation._readily_provable(
                self, check_transitive_pair=check_transitive_pair):
            return True

        # In the following, no worry about conflicts with assumptions
        # because the variable(s) will be bound by a quantifier.
        # (1) Vertices(H) ⊆ Vertices(G):
        from proveit.logic import And, Forall, InSet
        from proveit.logic.sets import Set
        from proveit.graphs import Vertices
        _v = safe_dummy_var(self, avoid_default_assumption_conflicts=False)
        # forall_{v in V(H)} v in V(G) => V(H) subseteq V(G):
        univ_quant_vertices = Forall(
                _v, InSet(_v, Vertices(self.supergraph)),
                domain=Vertices(self.subgraph))
        # (2) Edges(H) ⊆ Edges(G):
        from proveit.graphs import Edges
        _e = safe_dummy_var(self, avoid_default_assumption_conflicts=False)
        # forall_{e in E(H)} e in E(G) => E(H) subseteq E(G):
        univ_quant_edges = Forall(
                _e, InSet(_e, Edges(self.supergraph)),
                domain=Edges(self.subgraph))
        # (3) All H edge endpts are contained in V(H)
        _v1 = safe_dummy_var(avoid_default_assumption_conflicts=False)
        _v2 = safe_dummy_var(_v1, avoid_default_assumption_conflicts=False)
        # forall_{v1,v2 | {v1,v2} in E(H)}[v1, v2 in V(H)]
        univ_quant_uv = Forall((_v1,_v2),
                And(InSet(_v1, Vertices(self.subgraph)),
                    InSet(_v2, Vertices(self.subgraph))),
                conditions = [InSet(Set(_v1, _v2), Edges(self.subgraph))])
        return (univ_quant_vertices._readily_provable()
                & univ_quant_edges._readily_provable()
                & univ_quant_uv._readily_provable())

    # UNDER DEVELOPMENT
    @prover
    def conclude(self, **defaults_config):
        '''
        Try to conclude the subgraph claim H ⊆ G, using one of the
        following:
        (1) H = G (equal graphs are subgraphs of each other);
        (2) H ⊂ G (using H ⊂ G => H ⊆ G);
        (3) or satisfying the definition of H ⊆ G.
        '''
        from proveit import ProofFailure
        from proveit.logic import And, Equals, SetOfAll, SetEquiv
        from proveit.logic.sets import Set
        from proveit.graphs import Edges, Vertices
        from . import subgraph_via_equality

        # Equal graphs include each other.
        # Note that this doesn't apply generally to isomorphic graphs,
        # only literally EQUAL graphs.
        if Equals(*self.operands.entries).readily_provable() and (
                subgraph_via_equality.is_usable()):
            return self.conclude_via_equality()

        # for notational convenience
        from proveit import G, H
        H = self.subgraph
        G = self.supergraph

        # A proper subgraph is also a subgraph
        from . import relax_proper_subgraph
        if ProperSubgraph(H, G).readily_provable() and (
                relax_proper_subgraph.is_usable()):
            return self.conclude_via_proper_subgraph()

        # We have something more general. Try conclude_as_folded()
        return self.conclude_as_folded()

    @prover
    def conclude_via_equality(self, **defaults_config):
        from proveit import G, H
        from . import subgraph_via_equality
        return subgraph_via_equality.instantiate(
            {H: self.subgraph, G: self.supergraph})

    @prover
    def conclude_via_proper_subgraph(self, **defaults_config):
        from proveit import G, H
        from . import relax_proper_subgraph
        return relax_proper_subgraph.instantiate(
            {H: self.subgraph, G: self.supergraph})

    @prover
    def conclude_as_folded(self, **defaults_config):
        '''
        Derive this folded version, H ⊆ G, from the unfolded details:
            E(H) subset_eq [V(H)]^{2}
            AND V(H) subset_eq V(G);
            AND E(H) subset_eq E(G).
        '''
        from proveit import E, V
        from proveit.graphs import E_prime, V_prime
        from proveit.graphs import Edges, Vertices
        from . import fold_subgraph_def
        H = self.subgraph
        G = self.supergraph
        # No worry about conflicts with assumptions because the 
        # variable will be bound by a quantifier:
        return fold_subgraph_def.instantiate(
            {V: G.vertices, V_prime: H.vertices ,
             E: G.edges, E_prime: H.edges })
    
    # @prover
    # def unfold(self, elem_instance_var=None, **defaults_config):
    #     '''
    #     From A subset_eq B, derive and return (forall_{x in A} x in B).
    #     x will be relabeled if an elem_instance_var is supplied.
    #     '''
    #     from . import unfold_subset_eq
    #     if elem_instance_var is not None:
    #         temp_result = unfold_subset_eq.instantiate(
    #             {A: self.subset, B: self.superset})
    #         return temp_result.instantiate(
    #             {x: elem_instance_var}, num_forall_eliminations=0)
    #     return unfold_subset_eq.instantiate(
    #         {A: self.subset, B: self.superset})

    # @prover
    # def derive_superset_membership(self, element, **defaults_config):
    #     '''
    #     From A subset_eq B and element x in A, derive x in B.
    #     '''
    #     from . import unfold_subset_eq
    #     return unfold_subset_eq.instantiate(
    #         {A: self.subset, B: self.superset, x: element})

    # @prover
    # def derive_subset_nonmembership(self, element, **defaults_config):
    #     '''
    #     From A subset_eq B and element x not_in B, derive x not_in A.
    #     '''
    #     from . import refined_nonmembership
    #     return refined_nonmembership.instantiate(
    #         {A: self.subset, B: self.superset, x: element})
    
    # @prover
    # def apply_transitivity(self, other, **defaults_config):
    #     '''
    #     Apply a transitivity rule to derive from this A subseteq B
    #     expression and something of the form B subseteq C, B subset C,
    #     or B=C to obtain A subset C or A subseteq C as appropriate.
    #     '''
    #     from proveit.logic import Equals, SetEquiv, ProperSubset
    #     from . import (transitivity_subset_eq_subset,
    #                    transitivity_subset_subset_eq,
    #                    transitivity_subset_eq_subset_eq)
    #     other = as_expression(other)
    #     if isinstance(other, Equals) or isinstance(other, SetEquiv):
    #         return InclusionRelation.apply_transitivity(self, other)
    #     new_rel = None
    #     if other.subset == self.superset:
    #         if isinstance(other, ProperSubset):
    #             new_rel = transitivity_subset_eq_subset.instantiate(
    #                 {A: self.subset, B: self.superset, C: other.superset},
    #                 preserve_all=True)
    #         elif isinstance(other, SubsetEq):
    #             new_rel = transitivity_subset_eq_subset_eq.instantiate(
    #                 {A: self.subset, B: self.superset, C: other.superset},
    #                 preserve_all=True)
    #     elif other.superset == self.subset:
    #         if isinstance(other, ProperSubset):
    #             new_rel = transitivity_subset_subset_eq.instantiate(
    #                 {A: other.subset, B: other.superset, C: self.superset},
    #                 preserve_all=True)
    #         elif isinstance(other, SubsetEq):
    #             new_rel = transitivity_subset_eq_subset_eq.instantiate(
    #                 {A: other.subset, B: other.superset, C: self.superset},
    #                 preserve_all=True)
    #     if new_rel is None:
    #         raise ValueError(
    #             "Cannot perform transitivity with {0} and {1}!".
    #             format(self, other))
    #     return new_rel.with_mimicked_style(self)

    @relation_prover
    def deduce_in_bool(self, **defaults_config):
        '''
        Deduce and return that this [H Subgraph G] statement is
        in the Boolean set.
        '''
        from . import is_subgraph_is_bool
        _G_sub = self.supergraph
        _H_sub = self.subgraph
        is_bool_stmt = is_subgraph_is_bool.instantiate(
                {G: _G_sub, H: _H_sub})
        return (
            is_bool_stmt.inner_expr().element.with_matching_style(self)
            )

class ProperSubgraph(GraphInclusionRelation):
    '''
    ProperSubgraph(H, G) represents the claim that graph H is a
    proper subgraph of graph G, meaning that H is a subgraph of H
    (see the definition under Subgraph()), AND either V(H) is a 
    proper subset of V(G) and/or E(H) is a proper subset of E(G).

    Like the Subgraph class, the ProperSubgraph class has initially
    been modeled on the ProperSubset() class in logic/sets/inclusion,
    and uses the analogous GraphInclusionRelation() class (instead of
    the set-specific InclusionRelation()class).
    '''

    # Define the operator of the ProperSubgraph operation.
    # Following tradition in graph theory, we use the same operator ⊂
    # for proper subgraph as we use for proper subset, relying on the
    # context to distinguish the cases. We modify the string version
    # for clarity.
    _operator_ = Literal(string_format='proper_subgraph',
                         latex_format=r'\subset',
                         theory=__file__)

    # map left-hand-sides to Subgraph Judgments
    #   (populated in TransitivityRelation.derive_side_effects)
    known_left_sides = dict()
    # map right-hand-sides to Subgraph Judgments
    #   (populated in TransitivityRelation.derive_side_effects)
    known_right_sides = dict()

    def __init__(self, subgraph, graph, *, styles=None):
        '''
        Create the expression for (H ⊂ G).
        '''
        GraphInclusionRelation.__init__(
                self, ProperSubgraph._operator_,
                subgraph, graph, styles=styles)

    @staticmethod
    def reversed_operator_str(format_type):
        '''
        Reversing H ⊂ G gives G ⊃ H (subset symbol is changed to
        the supset symbol).
        '''
        return r'\supset' if format_type == 'latex' else 'proper_supergraph'

# def superset_eq(A, B):
#     '''
#     Return the expression representing (A superset_eq B), internally
#     represented as (B subset_eq A) but with a style that reverses
#     the direction.
#     '''
#     return SubsetEq(B, A).with_styles(direction = 'reversed')
