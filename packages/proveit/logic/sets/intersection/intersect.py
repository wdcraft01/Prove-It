from proveit import (equality_prover, ExprRange, Literal, Operation,
                     SimplificationDirectives, USE_DEFAULTS)
from proveit import i, j, k, m, n, x, A, B
from proveit.abstract_algebra.generic_methods import (
        apply_association_thm, apply_commutation_thm,
        apply_disassociation_thm, generic_permutation, group_commutation)


class Intersect(Operation):
    # operator of the Intersect operation
    _operator_ = Literal(
        string_format='intersect',
        latex_format=r'\cap',
        theory=__file__)

    _simplification_directives_ = SimplificationDirectives(
            ungroup=True)

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

    @equality_prover('consolidated_to_intersectall',
                     'consolidate_to_intersectall')
    def consolidation_to_intersectall(
            self, instance_param=None, **defaults_config):
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

    @equality_prover('commuted', 'commute')
    def commutation(self, init_idx=None, final_idx=None, **defaults_config):
        '''
        Deduce that this Intersect expression is equal to a form in
        which the operand at index init_idx has been moved to index
        final_idx. For example:

            (A ∩ B ∩ ... ∩ Y ∩ Z).commutation(1, -2)

        will produce: |-  (A ∩ B ∩ ... ∩ Y ∩ Z) = (A ∩ ... ∩ Y ∩ B ∩ Z).
        '''
        from . import commutation, leftward_commutation, rightward_commutation
        return apply_commutation_thm(
            self, init_idx, final_idx, commutation,
            leftward_commutation, rightward_commutation)

    @equality_prover('group_commuted', 'group_commute')
    def group_commutation(self, init_idx, final_idx, length,
                          disassociate=True, **defaults_config):
        '''
        Deduce that this Intersect expression is equal to a form in
        which the operands at indices [init_idx, init_idx+length) have
        been moved to [final_idx, final_idx+length).
        It will do this by performing association first.
        If disassociate is True (the default), the specified operands
        will be disassociated before returning.
        '''
        return group_commutation(
            self, init_idx, final_idx, length, disassociate=disassociate)

    @equality_prover('moved', 'move')
    def permutation_move(self, init_idx=None, final_idx=None,
                         **defaults_config):
        '''
        Deduce that this Intersect expression is equal to a form in
        which the operand at index init_idx has been moved to final_idx.
        For example, (A ∩ B ∩ ... ∩ Y ∩ Z).permutation_move(1, -2) will
        produce: |- (A ∩ B ∩ ... ∩ Y ∩ Z) = (A ∩ ... ∩ Y ∩ B ∩ Z),
        moving operand B from position index 1 to position index -2.
        For the Intersect class, this method just immediately calls the
        Intersect.commutation() method; we keep the permutation_move()
        method because it is used by the permutations machinery
        available in abstract_algebra/generic_methods.py.
        '''
        return self.commutation(init_idx=init_idx, final_idx=final_idx)

    @equality_prover('permuted', 'permute')
    def permutation(self, new_order=None, cycles=None, **defaults_config):
        '''
        Deduce that this Intersect expression is equal to a Union in
        which the operands at indices 0, 1, …, n-1 have been reordered
        as specified EITHER by the new_order list OR by the cycles list
        parameter. For example,

            (A ∩ B ∩ C ∩ D).permutation(new_order=[0, 2, 3, 1])

        and (A ∩ B ∩ C ∩ D).permutation(cycles=[(1, 2, 3)])

        would both return ⊢ (A ∩ B ∩ C ∩ D) = (A ∩ C ∩ D ∩ B).
        '''
        return generic_permutation(self, new_order, cycles)

    @equality_prover('associated', 'associate')
    def association(self, start_idx, length, **defaults_config):
        '''
        Deduce that this Intersect expression is equal to a form in
        which operands in the range [start_idx, start_idx+length) are
        grouped together. For example,

            (A ∩ B ∩ C ∩ D ∩ E ∩ ... ∩ Y ∩ Z).association(2, 3)

        would derive and return:

            |- (A ∩ B ∩ C ∩ D ∩ E ∩ ... ∩ Y ∩ Z)
               = (A ∩ B ∩ (C ∩ D ∩ E) ∩ ... ∩ Y ∩ Z)
        '''
        from . import association
        return apply_association_thm(self, start_idx, length, association)

    @equality_prover('disassociated', 'disassociate')
    def disassociation(self, idx, **defaults_config):
        '''
        Deduce that this Intersect expression is equal to a form in
        which the operand at index idx is no longer grouped together.
        For example,

            (A ∩ B ∩ (C ∩ D ∩ E) ∩ ... ∩ Y ∩ Z).disassociation(2)

        would derive and return:

            |- (A ∩ B ∩ (C ∩ D ∩ E) ∩ ... ∩ Y ∩ Z)
               = (A ∩ B ∩ C ∩ D ∩ E ∩ ... ∩ Y ∩ Z)
        
        Multiple indices can be provided for multiple disassociations
        simultaneously, e.g. expr.disassociation(2, 3, 4)
        '''
        from . import disassociation
        return apply_disassociation_thm(self, idx, disassociation)

    @equality_prover('distributed_over_union',
                     'distribute_over_union')
    def distribution_over_union(self, target='right', **defaults_config):
        '''
        Given self = Intersect(A, Union(B1, B2, ..., Bn)), and
        target='right' (the default), derive and return the equality
        between self and its distributed form:

        |- Intersect(A, Union(B1, B2, ..., Bn))
           = Union(Intersect(A, B1),..., Intersect(A, Bn))

        A could be a single set or some more complex expression
        representing a set, but will be kept as a unit.

        Similarly, given self = Intersect(Union(A1, A2, ..., Am), B),
        and target='left', derive and return the equality between self
        and its distributed form:

        |- Intersect(Union(A1, A2, ..., Am), B)
           = Union(Intersect(A1, B),..., Intersect(Am, B))

        For a full cross distribution of both sides, use
        target = 'both'.
        '''
        from proveit.logic.sets import Union
        from proveit.numbers import two
        if not (self.operands.is_double() and
               (isinstance(self.operands[0], Union)
                or isinstance(self.operands[1], Union))):
            raise ValueError(
                    "'Intersect.distribution_over_union()' method "
                    "only valid for Intersect() with 2 operands with at "
                    "least one of the operands being a Union().")

        # Case: target = 'right' (the default)
        if target == 'right':
            if not isinstance(self.operands[1], Union):
                raise ValueError(
                        "'Intersect.distribution_over_union()'' method "
                        "with target = 'right' only valid for Intersect() "
                        "with second of two operands being a Union().")
            from . import distribution_over_union_right
            _n_sub = self.operands[1].operands.num_elements()
            _A_sub = self.operands[0]
            _B_sub = self.operands[1].operands
            return distribution_over_union_right.instantiate(
                    {n:_n_sub, A:_A_sub, B:_B_sub})

        # Case: target = 'left'
        if target == 'left':
            if not isinstance(self.operands[0], Union):
                raise ValueError(
                        "'Intersect.distribution_over_union()'' method "
                        "with target = 'left' only valid for Intersect() "
                        "with first of two operands being a Union().")
            from . import distribution_over_union_left
            from proveit.numbers import num
            _m_sub = self.operands[0].operands.num_elements()
            _A_sub = self.operands[0].operands
            _B_sub = self.operands[1]
            return distribution_over_union_left.instantiate(
                    {m:_m_sub, A:_A_sub, B:_B_sub})

        # Case: target = 'both'
        if target == 'both':
            if not (isinstance(self.operands[0], Union)
                    and isinstance(self.operands[1], Union)):
                raise ValueError(
                        "'Intersect.distribution_over_union()' method "
                        "with target = 'both' only valid for Intersect() "
                        " with two operands, each of which is a Union().")

            # Both operands are Union()
            if (isinstance(self.operands[0], Union)
                and isinstance(self.operands[1], Union)):
                from . import distribution_over_union_left_right
                _m_sub = self.operands[0].operands.num_elements()
                _n_sub = self.operands[1].operands.num_elements()
                _A_sub = self.operands[0].operands
                _B_sub = self.operands[1].operands
                print(f"_m_sub = {_m_sub}")
                print(f"_n_sub = {_n_sub}")
                print(f"_A_sub = {_A_sub}")
                print(f"_B_sub = {_B_sub}")
                return distribution_over_union_left_right.instantiate(
                        {m:_m_sub, n:_n_sub, A:_A_sub, B:_B_sub})

            # Both operands are IntersectAll()
            # TBA
