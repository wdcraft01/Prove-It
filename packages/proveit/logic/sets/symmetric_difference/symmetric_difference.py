from proveit import Literal, Operation, USE_DEFAULTS, relation_prover
from proveit import m, n, A, S, x


class SymmetricDifference(Operation):
    '''
    SymmetricDifference(A1,...,An) represents the symmetric difference
    of the operand sets A1, ..., An, displayed symbolically as:

        A1 ∆ A2 ∆ ... ∆ An

    The symmetric difference of two sets A and B, represented by
    SymmetricDifference(A,B) and displayed as A ∆ B, is the sets of
    elements that are in set A or in set B but not in both. In the
    more general case, A1 ∆ A2 ∆ ... ∆ An is the set of elements that
    appear in exactly an odd number of the operand sets A1,...,An.
    '''

    # The literal operator of the SymmetricDifference operation
    _operator_ = Literal(
        string_format="SymDiff",
        latex_format=r'\Delta',
        theory=__file__)

    def __init__(self, *operands, styles=None):
        '''
        Represent the symmetric difference of any number of sets:
        A1 ∆ A2 ∆ ... ∆ An.
        '''
        Operation.__init__(self, SymmetricDifference._operator_,
                           operands, styles=styles)

    def membership_object(self, element):
        from .symmetric_difference_membership import (
                SymmetricDifferenceMembership)
        return SymmetricDifferenceMembership(element, self)

    def nonmembership_object(self, element):
        from .symmetric_difference_membership import (
                SymmetricDifferenceNonmembership)
        return SymmetricDifferenceNonmembership(element, self)

    # @relation_prover
    # def deduce_superset_eq_relation(self, superset, **defaults_config):
    #     # Check for special case of a union subset
    #     # A_1 union ... union ... A_m \subseteq S
    #     from . import union_inclusion
    #     _A = self.operands
    #     _m = _A.num_elements()
    #     _S = superset
    #     return union_inclusion.instantiate(
    #                 {A:_A, m:_m, S:_S})
            