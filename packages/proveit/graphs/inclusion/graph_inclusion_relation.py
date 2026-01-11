from proveit import USE_DEFAULTS, prover
from proveit.relation import (
    TransitiveRelation, total_ordering)


class GraphInclusionRelation(TransitiveRelation):
    r'''
    Base class for all strict and non-strict graph containment
    relations (subgraph and proper subgraph relations).
    This is modeled on the InclusionRelation() class found in
    logic/sets/incusion/inclusion_relation.py.
    Do not construct an object of this class directly!
    Instead, use Subgraph or ProperSubgraph.
    '''

    def __init__(self, operator, lhs, rhs, *, styles):
        TransitiveRelation.__init__(self, operator, lhs, rhs,
                                    styles=styles)
        self.subgraph = self.operands[0]
        self.supergraph = self.operands[1]

    @staticmethod
    def WeakRelationClass():
        from .subgraph import Subgraph
        return Subgraph

    @staticmethod
    def StrongRelationClass():
        from .subgraph import ProperSubgraph
        return ProperSubgraph

    # Uncomment once some details are worked out.
    # Equivalent graphs might be graphs that are the same up to
    # a re-labeling of the vertices. Equal graphs would be stronger,
    # having the exact same labelings.
    # @staticmethod
    # def EquivalenceClass():
    #     from proveit.logic.sets.equivalence import SetEquiv
    #     return SetEquiv
    
    def side_effects(self, judgment):
        '''
        In addition to the TransitiveRelation side-effects, also
        attempt derive_relaxed (if applicable) and derive_reversed.
        '''
        for side_effect in TransitiveRelation.side_effects(self, judgment):
            yield side_effect
        if hasattr(self, 'derive_relaxed'):
            yield self.derive_relaxed
    
    # @staticmethod
    # @prover
    # def apply_transitivity(self, other, **defaults_config):
    #     '''
    #     apply_transitivity(Subgraph(A,B), Equals(B,C)) 
    #     returns Subgraph(A,C)
    #     '''
    #     from proveit.logic import Equals, SetEquiv, SubsetEq
    #     if isinstance(other, Equals):
    #         return TransitiveRelation.apply_transitivity(self, other)
    #     if isinstance(other, SetEquiv):
    #         # From set equivalence, derive the appropriate subset_eq
    #         # so we can use normal subset transitivity.
    #         if other.lhs == self.superset or other.rhs == self.subset:
    #             # EITHER (A subset B) and (B set_equiv C) 
    #             # OR (A subset B) and (C set_equiv A)
    #             other_as_subset_eq = SubsetEq(*other.operands.entries)
    #         elif other.rhs == self.superset or other.lhs == self.subset:
    #             # EITHER (A subset B) and (C set_equiv B)
    #             # OR (A subset B) and (A set_equiv C)
    #             other_as_subset_eq = SubsetEq(
    #                     *reversed(other.operands.entries))
    #         else:
    #             raise ValueError("Unable to apply transitivity between %s "
    #                              "and %s."%(self, other))
    #         return self.apply_transitivity(other_as_subset_eq)

# def inclusion_ordering(*relations):
#     '''
#     Return a conjunction of subgraph and proper subgraph ordering
#     relations with a total-ordering style; for example,
#     A proper_subgraph B = C = D subgraph E
#     '''
#     from proveit.logic.sets.equivalence import SetEquiv
#     for relation in relations:
#         if (not isinstance(relation, InclusionRelation) and
#                not isinstance(relation, SetEquiv)):
#             raise TypeError("For a set inclusion ordering expression, "
#                             "all relations must be either InclusionRelation "
#                             "or SetEquiv objects.")
#     return total_ordering(*relations)
