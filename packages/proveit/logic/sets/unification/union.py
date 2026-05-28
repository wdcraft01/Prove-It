from proveit import (equality_prover, Literal, Operation, USE_DEFAULTS,
                     relation_prover)
from proveit import m, n, A, S, x


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
            