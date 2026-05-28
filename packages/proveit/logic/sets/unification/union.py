from proveit import (equality_prover, ExprRange, Literal, Operation,
                     USE_DEFAULTS, relation_prover)
from proveit import i, j, k, m, n, A, S, x


class Union(Operation):
    # operator of the Intersect operation
    _operator_ = Literal(
        string_format='union',
        latex_format=r'\cup',
        theory=__file__)

    def __init__(self, *operands, styles=None):
        '''
        Union any number of sets: A union B union C
        '''
        Operation.__init__(self, Union._operator_, operands,
                           styles=styles)

    def membership_object(self, element):
        from .union_membership import UnionMembership
        return UnionMembership(element, self)

    def nonmembership_object(self, element):
        from .union_membership import UnionNonmembership
        return UnionNonmembership(element, self)

    @relation_prover
    def deduce_superset_eq_relation(self, superset, **defaults_config):
        # Check for special case of a union subset
        # A_1 union ... union ... A_m \subseteq S
        from . import union_inclusion
        _A = self.operands
        _m = _A.num_elements()
        _S = superset
        return union_inclusion.instantiate(
                    {A:_A, m:_m, S:_S})

    @equality_prover('unary_reduced', 'unary_reduce')
    def unary_reduction(self, **defaults_config):
        '''
        Given self = [Union(A)], derive and return the equality
        between self and A (i.e., |- Union(A) = A).
        '''
        from . import unary_union_reduction
        if not self.operands.is_single():
            raise ValueError("Union expression must have a single operand "
                             "in order to invoke unary_reduction. ")
        operand = self.operands[0]
        return unary_union_reduction.instantiate({A: operand})

    @equality_prover('redundancy_reduced', 'redundancy_reduce')
    def redundancy_reduction(self, **defaults_config):
        '''
        Given self = Union(A, A, ..., A), derive and return the
        equality between self A:

            |- Union(A, A, ..., A) = A
        '''

        # Case (1) Union(A, A)
        if (len(self.operands) == 2):
            if self.operands[0] == self.operands[1]:
                from . import redundant_union_binary
                _A_sub = self.operands[0]
                return redundant_union_binary.instantiate({A: _A_sub})

        # Case (2) Union(A, ..., A) but not using ExprRange
        # TBA

        # Case (3) Union(A,...,A) using ExprRange as single operand
        if (self.operands.num_entries() == 1
            and isinstance(self.operands[0], ExprRange)):

            expr_range = self.operands[0]
            _A_sub = expr_range.body

            from proveit.numbers import one

            if expr_range.true_start_index == one:
                from . import redundant_union_range
                return redundant_union_range.instantiate(
                    {n: expr_range.true_end_index, A: _A_sub})
            else:
                from . import redundant_union_range_general
                _i_sub = expr_range.true_start_index
                _j_sub = expr_range.true_end_index
                return redundant_union_range_general.instantiate(
                    {i:_i_sub, j:_j_sub, A:_A_sub})

    @equality_prover('unionall_equated', 'unionall_equate')
    def unionall_equation(self, instance_param=None, **defaults_config):
        '''
        From self = Union(A(i), A(i+1), ..., A(j)) using a single
        ExprRange operand, derive and return the equality of self with
        its alternative UnionAll form:

            |- Union(A(i), A(i+1), ..., A(j))
               = Unionall(k, A(k), for k in {i,...,j})

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
                    "'Union.unionall_equation()' method may only be "
                    "used on a Union with a single ExprRange operand.")

        from . import union_eq_unionall
        expr_range = self.operands[0]
        _i_sub = expr_range.true_start_index
        _j_sub = expr_range.true_end_index
        _k_sub = (expr_range.parameter if instance_param is None
                  else instance_param)
        _A_sub = expr_range.lambda_map

        proven_unionall = union_eq_unionall.instantiate(
                {i:_i_sub, j:_j_sub, k:_k_sub, A:_A_sub})
        
        return proven_unionall

            