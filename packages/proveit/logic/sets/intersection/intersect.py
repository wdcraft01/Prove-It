from proveit import equality_prover, Literal, Operation, USE_DEFAULTS
from proveit import n, x, A


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
