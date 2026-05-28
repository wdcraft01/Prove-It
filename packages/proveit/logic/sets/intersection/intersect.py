from proveit import (equality_prover, ExprRange, Literal, Operation,
                     USE_DEFAULTS)
from proveit import i, j, k, n, x, A


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

    @equality_prover('intersectall_equated', 'intersectall_equate')
    def intersectall_equation(self, instance_param=None, **defaults_config):
        '''
        From self = Intersect(A(i), A(i+1), ..., A(j)) using a single
        ExprRange operand, derive and return the equality of self with
        its alternative IntersectAll form:

            |- Union(A(i), A(i+1), ..., A(j))
               = IntersectAll(k, A(k), for k in {i,...,j})

        If 'instance_param' is provided, use it as the 'k' parameter.
        Otherwise, use the parameter of the given ExprRange (which
        will be some generic canonical such as '_a').
        '''
        # from proveit import ExprRange
        # from proveit.logic import InSet
        # from proveit.numbers import Interval
        if (self.operands.num_entries() != 1
            or not isinstance(self.operands[0], ExprRange)):
            raise ValueError(
                    "'Intersect.intersectall_equation()' method may only be "
                    "used on an Intersect with a single ExprRange operand.")

        from . import intersect_eq_intersectall
        expr_range = self.operands[0]
        _i_sub = expr_range.true_start_index
        _j_sub = expr_range.true_end_index
        _k_sub = (expr_range.parameter if instance_param is None
                  else instance_param)
        _A_sub = expr_range.lambda_map

        proven_intersectall = intersect_eq_intersectall.instantiate(
                {i:_i_sub, j:_j_sub, k:_k_sub, A:_A_sub})
        
        return proven_intersectall
