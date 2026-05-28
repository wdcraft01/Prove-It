from proveit import (equality_prover, ExprRange, Literal, Operation,
                     USE_DEFAULTS)
from proveit import i, j, n, x, A


class Intersect(Operation):
    # operator of the Intersect operation
    _operator_ = Literal(
        string_format='intersect',
        latex_format=r'\cap',
        theory=__file__)

    def __init__(self, *operands, styles=None):
        '''
        Intersect any number of set: A intersect B intersect C
        '''
        Operation.__init__(self, Intersect._operator_, operands,
                           styles=styles)

    def membership_object(self, element):
        from .intersect_membership import IntersectMembership
        return IntersectMembership(element, self)

    def nonmembership_object(self, element):
        from .intersect_membership import IntersectNonmembership
        return IntersectNonmembership(element, self)

    @equality_prover('unary_reduced', 'unary_reduce')
    def unary_reduction(self, **defaults_config):
        '''
        Given self = [Intersect(A)], derive and return the equality
        between self and A (i.e., |- Intersect(A) = A).
        '''
        from . import unary_intersect_reduction
        if not self.operands.is_single():
            raise ValueError(
                    "Intersection expression must have a single operand "
                    "in order to invoke unary_reduction. ")
        operand = self.operands[0]
        return unary_intersect_reduction.instantiate({A: operand})

    @equality_prover('redundancy_reduced', 'redundancy_reduce')
    def redundancy_reduction(self, **defaults_config):
        '''
        Given self = Intersect(A, A, ..., A), derive and return the
        equality between self A:

            |- Intersect(A, A, ..., A) = A
        '''

        # Case (1) Intersect(A, A)
        if (len(self.operands) == 2):
            if self.operands[0] == self.operands[1]:
                from . import redundant_intersection_binary
                _A_sub = self.operands[0]
                return redundant_intersection_binary.instantiate({A: _A_sub})

        # Case (2) Intersect(A, ..., A) but not using ExprRange
        # TBA

        # Case (3) Intersect(A,...,A) using ExprRange as single operand
        if (self.operands.num_entries() == 1
            and isinstance(self.operands[0], ExprRange)):

            expr_range = self.operands[0]
            _A_sub = expr_range.body

            from proveit.numbers import one

            if expr_range.true_start_index == one:
                from . import redundant_intersection_range
                return redundant_intersection_range.instantiate(
                        {n: expr_range.true_end_index, A: _A_sub})
            else:
                from . import redundant_intersection_range_general
                _i_sub = expr_range.true_start_index
                _j_sub = expr_range.true_end_index
                return redundant_intersection_range_general.instantiate(
                        {i:_i_sub, j:_j_sub, A:_A_sub})
