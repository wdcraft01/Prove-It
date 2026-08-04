from proveit import USE_DEFAULTS, equality_prover, prover
from proveit.logic import SetMembership, SetNonmembership
from proveit.numbers import num
from proveit import m, n, A, x


class SymmetricDifferenceMembership(SetMembership):
    '''
    Defines methods that apply to membership in the symmetric
    difference of sets.
    The symmetric difference of two sets A and B, represented by
    SymmetricDifference(A,B) and displayed as A ∆ B, is the set of
    elements that are in set A or in set B but not in both. In the
    more general case, A1 ∆ A2 ∆ ... ∆ An is the set of elements that
    appear in exactly an odd number of the operand sets A1,...,An.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    def side_effects(self, judgment):
        '''
        Unfold the SymmetricDifference set membership as a side-effect.
        '''
        yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Deduce and return 
            [x in (A1 ∆ A2 ∆ ... ∆ An)] = 
            [(x in A1) XOr (x in A2) XOr ... XOr (x in An)]
        where self = [x in (A1 ∆ A2 ∆ ... ∆ An)].
        '''
        from . import sym_diff_def
        element = self.element
        operands = self.domain.operands
        _A_sub = operands
        _n_sub = _A_sub.num_elements()
        return sym_diff_def.instantiate(
                {n: _n_sub, x: element, A: _A_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From self=[elem in (A1 ∆ A2 ∆ ... ∆ An)], return the
        Expression (not a Judgment):
    
            [(elem in A1) XOr (elem in A2) XOr ... XOr (elem in An)].
        '''
        from proveit.logic import XOr, InSet
        element = self.element
        return XOr(*self.domain.operands.map_elements(
                lambda subset : InSet(element, subset)))

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [elem in (A1 ∆ A2 ∆ ... ∆ An)], and knowing or
        assuming self to be True, derive and return
        [(elem in A1) XOr (elem in A2) XOr ... XOr (elem in An)].
        '''
        from . import membership_unfolding
        element = self.element
        operands = self.domain.operands
        _A_sub = operands
        _n_sub = _A_sub.num_elements()
        return membership_unfolding.instantiate(
                {n: _n_sub, x: element, A: _A_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        Called on self = [elem in (A1 ∆ A2 ∆ ... ∆ An)], and knowing or
        assuming

            [(elem in A1) XOr (elem in A2) XOr ... XOr (elem in An)],

        derive and return self.
        '''
        from . import membership_folding
        element = self.element
        operands = self.domain.operands
        _A_sub = operands
        _n_sub = _A_sub.num_elements()
        return membership_folding.instantiate(
                {n: _n_sub, x: element, A: _A_sub})


class SymmetricDifferenceNonmembership(SetNonmembership):
    '''
    Defines methods that apply to non-membership in a symmetric
    difference of sets.
    Except for the __init__(), method development here is postponed
    for now, leaving the analogous UnionNonmembership class methods
    here as placeholders.
    '''

    def __init__(self, element, domain):
        SetNonmembership.__init__(self, element, domain)

#     def side_effects(self, judgment):
#         '''
#         Currently no side-effects for union nonmembership.
#         '''
#         return
#         yield

#     @equality_prover('defined', 'define')
#     def definition(self, **defaults_config):
#         '''
#         From self=[elem not in (A U B U ...)], deduce and return
#             |- [elem not in (A U B U ...)] = 
#             [(element not in A) and (element not in B) and ...].
#         '''
#         from . import nonmembership_equiv
#         element = self.element
#         operands = self.domain.operands
#         _A = operands
#         _m = _A.num_elements()
#         return nonmembership_equiv.instantiate(
#             {m: _m, x: element, A: _A}, auto_simplify=False)

#     def as_defined(self):
#         '''
#         From self=[elem not in (A U B U ...)], return
#         [(element not in A) and (element not in B) and ...].
#         '''
#         from proveit.logic import And, NotInSet
#         element = self.element
#         return And(*self.domain.operands.map_elements(
#                 lambda subset : NotInSet(element, subset)))

#     @prover
#     def conclude(self, **defaults_config):
#         '''
#         Called on the self = [elem not in (A U B U ...)], from known
#         or assumed [element not in A] and [element not in B] ...,
#         derive and return self.
#         '''
#         from . import nonmembership_folding
#         element = self.element
#         operands = self.domain.operands
#         _A = operands
#         _m = _A.num_elements()
#         return nonmembership_folding.instantiate(
#             {m: _m, x: element, A: _A})
