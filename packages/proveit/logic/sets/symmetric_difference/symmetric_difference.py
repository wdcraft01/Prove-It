from proveit import (
        equality_prover, Literal, Operation, USE_DEFAULTS,
        relation_prover, SimplificationDirectives, TransRelUpdater)
from proveit import l, m, n, x, A, B, C, S, X
from proveit.abstract_algebra.generic_methods import (
        apply_association_thm, apply_commutation_thm,
        apply_disassociation_thm, generic_permutation, group_commutation,
        sorting_and_combining_like_operands)


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

    _simplification_directives_ = SimplificationDirectives(
            ungroup=True)

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

    @equality_prover('shallow_simplified', 'shallow_simplify')
    def shallow_simplification(self, *, must_evaluate=False,
                               **defaults_config):
        '''
        Returns a proven simplification equation for this
        SymmetricDifference expression, assuming the operands have
        been simplified, according to the simplification directives
        as follows:

        * If ungroup is True (the default), disassociate nested
          SymmetricDifferences.

        * If sorting is required, sort operands according to the
          order_key_fn, where the key is simply the operand itself.

        * Eliminate any EmptySet operands (assuming this leaves at
          least one non-EmptySet operand), since:

              A ∆ EmptySet = EmptySet ∆ A = A

        * Eliminate pairs of identical operands, since A ∆ A = EmptySet
          and EmptySet serves as an identity (see item above).
        '''

        # Empty SymmetricDifference, ∆()
        if self.operands.num_entries() == 0:
            from . import empty_sym_diff_eval
            # SymmetricDifference() = EmptySet
            return empty_sym_diff_eval

        # Unary SymmetricDifference, ∆(A)
        if self.operands.is_single():
            # ∆(A) = A
            from . import unary_sym_diff_reduction
            _A_sub = self.operands[0]
            return unary_sym_diff_reduction.instantiate({A:_A_sub})

        expr = self
        # for convenience in updating our equation, begining with
        # self = self
        eq = TransRelUpdater(self)

        # Ungroup the expression (disassociate nested ∆s)
        if SymmetricDifference._simplification_directives_.ungroup:
            idx = 0
            length = expr.operands.num_entries() - 1
            while idx < length:
                # loop through all operands
                if isinstance(expr.operands[idx], SymmetricDifference):
                    # if it is grouped, ungroup it
                    expr = eq.update(expr.disassociation(
                                idx, preserve_all=True))
                else:
                    idx += 1
                length = expr.operands.num_entries()

        # Likeness of operands is simply equality of operands ---
        # i.e., two operands are "alike" if they are equal
        likeness_key_fn = lambda operand : operand

        # Combine like operands: A ∆ A = EmptySet
        expr = eq.update(sorting_and_combining_like_operands(
                expr, order_key_fn=lambda likeness_key : 0,
                likeness_key_fn=likeness_key_fn,
                preserve_likeness_keys=True, auto_simplify=True))

        if isinstance(expr, SymmetricDifference):
            # Remove any remaining EmptySets
            expr = eq.update(expr.empty_set_eliminations())

        if not isinstance(expr, SymmetricDifference):
            # Simplified to something other than a SymmetricDifference.
            # We're done here.
            return eq.relation

        return eq.relation # Might simply be self = self.

    @equality_prover('eliminated_empty_sets', 'eliminate_empty_sets')
    def empty_set_eliminations(self, **defaults_config):
        '''
        Equality prover method that derives a simplification in which
        EmptySet operands are eliminated. For example,

            SymmetricDifference(A, EmptySet, B, EmptySet, C, EmptySet).
            empty_set_eliminations()

        derives and returns: |- (A ∆ ∅ ∆ B ∆ ∅ ∆ C ∆ ∅) = (A ∆ B ∆ C).
        '''

        from proveit.logic.sets import EmptySet
        expr = self

        # A convenience to allow successive updates to the equation
        # via transitivities (starting with self=self).
        eq = TransRelUpdater(self)

        # Work in reverse order so indices don't need to be updated.
        for rev_idx, operand in enumerate(reversed(self.operands.entries)):
            if operand == EmptySet:
                idx = self.operands.num_entries() - rev_idx - 1
                expr = eq.update(expr.empty_set_elimination(
                        idx, preserve_all=True))
                if not isinstance(expr, SymmetricDifference):
                    # can't do an elimination if reduced to a single term.
                    break

        return eq.relation

    @equality_prover('eliminated_empty_set', 'eliminate_empty_set')
    def empty_set_elimination(self, idx, **defaults_config):
        '''
        Equality prover method that derives a simplification in which
        a single EmptySet operand, at the given index, is eliminated.
        For example,

            SymmetricDifference(A, B, EmptySet, C).
            empty_set_elimination(2)

        would return:
                       |- (A ∆ B ∆ ∅ ∆ C) = (A ∆ B ∆ C)
        '''
        from proveit.logic.sets import EmptySet
        from . import (sym_diff_with_empty_left, sym_diff_with_empty_right,
                       sym_diff_with_empty)

        if self.operands[idx] != EmptySet: # might need isinstance?
            raise ValueError(
                f"Operand at the provided index idx = {idx} expected "
                f"to be an EmptySet for {self}")

        if self.operands.is_double():
            if idx == 0:
                return sym_diff_with_empty_left.instantiate(
                        {A: self.operands[1]})
            else:
                return sym_diff_with_empty_right.instantiate(
                        {A: self.operands[0]})

        # Else we have more than two operands
        _A_sub = self.operands[:idx]
        _B_sub = self.operands[idx + 1:]
        _m_sub = _A_sub.num_elements()
        _n_sub = _B_sub.num_elements()
        return sym_diff_with_empty.instantiate(
                {m: _m_sub, n: _n_sub, A: _A_sub, B: _B_sub})

    @equality_prover('combined_operands', 'combine_operands')
    def combining_operands(self, start_idx=None, end_idx=None,
                           **defaults_config):
        '''
        combining_operands() is called from generic_methods.py,
        providing a formula/algorithm for combining operands in the
        context of a SymmetricDifference.
        For a SymmetricDifference, combining operands essentially
        means an annihilation process where A ∆ A = EmptySet,
        which can then itself be eliminated since the EmptySet serves
        as the identity element for symmetric difference.
        Notice that "like terms" here means identical terms, and
        combining like terms amounts to eliminating pairs of like
        terms.
        '''

        from proveit.abstract_algebra.generic_methods import (
                common_likeness_key)
        from proveit.logic import Equals
        from proveit.numbers import one

        # If the start_idx and/or end_idx has been specified
        if start_idx is not None or end_idx is not None:

            # Compensate for potential missing indices in this block:
            # omission of either start or end idx defaults to a pair
            # of contiguous operands
            if end_idx is None:
                end_idx = min(start_idx + 1, self.operands.num_entries())
            elif start_idx is None:
                start_idx = max(0, end_idx - 1)

            assoc_length = end_idx - start_idx + 1

            # Problem if in fact we're simply specifying ALL
            # of the operands, so we check that we're actually
            # dealing with a subset of the operands
            if assoc_length != self.operands.num_elements().as_int():

                # Associate the operands intended for combination.
                # Warning: 2nd arg of association() is length not index.
                grouped = self.association(start_idx, assoc_length)
                # isolate the targeted factors and combine them as desired
                # using call to this same method
                inner_combination = (
                        grouped.rhs.operands[start_idx].
                        combining_operands())
                # substitute the combined operands back into the
                # grouped expression and return the deduced equality
                return inner_combination.sub_right_side_into(grouped)

        # likeness of operands is simply equality of operands ---
        # i.e. two operands are "alike" if they are equal
        likeness_key_fn = lambda operand : operand

        if self.operands.num_entries()==0:
            # [∆]() = EmptySet
            from . import empty_sym_diff_eval
            return empty_sym_diff_eval

        operands = list(self.operands.entries)

        # We try to recursively reduce the number of identical
        # operands being considered by repeatedly dealing with
        # the operands pair-wise. 
        _num_operands = self.operands.num_elements().as_int()

        expr = self
        # For convenience in updating our equation, begining with
        # self = self
        eq = TransRelUpdater(self)

        while _num_operands >= 2:
            # Successively eliminate a sub-group of two operands:
            # A ∆ A = EmptySet, and EmptySet can be eliminated.

            from . import sym_diff_reduction
            from proveit.numbers import zero
            _l_sub = zero
            _m_sub = zero
            _A_sub = ()
            _B_sub = ()
            _C_sub = self.operands[2:]
            _n_sub = _C_sub.num_elements()
            _X_sub = self.operands[0]
            inst = sym_diff_reduction.instantiate(
                {l:_l_sub, m:_m_sub, n:_n_sub,
                 A:_A_sub, B:_B_sub, C:_C_sub, X:_X_sub})
            expr = eq.update(inst)
            if isinstance(expr, SymmetricDifference):
                _num_operands = expr.operands.num_elements().as_int()
            else:
                return eq.relation

        return Equals(self, self).conclude_via_reflexivity()

    @equality_prover('commuted', 'commute')
    def commutation(self, init_idx=None, final_idx=None, **defaults_config):
        '''
        Deduce that this SymmetricDifference expression is equal to a
        form in which the operand at index init_idx has been moved to
        index final_idx.
        For example, (A ∆ B ∆ ... ∆ Y U Z).commutation(1, -2) will
        produce: |-  (A ∆ B ∆ ... ∆ Y U Z) = (A ∆ ... ∆ Y U B U Z).
        '''
        from . import commutation, leftward_commutation, rightward_commutation
        return apply_commutation_thm(
            self, init_idx, final_idx, commutation,
            leftward_commutation, rightward_commutation)

    @equality_prover('group_commuted', 'group_commute')
    def group_commutation(self, init_idx, final_idx, length,
                          disassociate=True, **defaults_config):
        '''
        Deduce that this SymmetricDifference expression is equal to a
        form in which the operands at indices

            [init_idx, init_idx+length)

        (notice the right open interal) have been moved to

            [final_idx, final_idx+length).

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
        Deduce that this SymmetricDifference expression is equal to a
        form in which the operand at index init_idx has been moved to
        final_idx. For example,

            (A ∆ B ∆ ... ∆ Y ∆ Z).permutation_move(1, -2)

        will produce: |- (A ∆ B ∆ ... ∆ Y ∆ Z) = (A ∆ ... ∆ Y ∆ B ∆ Z),
        moving operand B from position index 1 to position index -2.
        For the SymmetricDifference class, this method just immediately
        calls the SymmetricDifference.commutation() method; we keep
        the permutation_move() method because it is used by the
        permutations machinery available in
        abstract_algebra/generic_methods.py.
        '''
        return self.commutation(init_idx=init_idx, final_idx=final_idx)

    @equality_prover('permuted', 'permute')
    def permutation(self, new_order=None, cycles=None, **defaults_config):
        '''
        Deduce that this SymmetricDifference expression is equal to a
        SymmetricDifference in which the operands at indices
        0, 1, …, n-1 have been reordered as specified EITHER by the
        new_order list OR by the cycles list parameter. For example,

            (A ∆ B ∆ C ∆ D).permutation(new_order=[0, 2, 3, 1])

        and (A ∆ B ∆ C ∆ D).permutation(cycles=[(1, 2, 3)])

        would both return ⊢ (A ∆ B ∆ C ∆ D) = (A ∆ C ∆ D ∆ B).
        '''
        return generic_permutation(self, new_order, cycles)

    @equality_prover('associated', 'associate')
    def association(self, start_idx, length, **defaults_config):
        '''
        Deduce that this SymmetricDifference expression is equal to
        a form in which operands in the range

            [start_idx, start_idx+length)

        are grouped together. For example,

            (A ∆ B ∆ C ∆ D ∆ E ∆ ... ∆ Y ∆ Z).association(2, 3)

        would derive and return:

            |- (A ∆ B ∆ C ∆ D ∆ E ∆ ... ∆ Y ∆ Z)
               = (A ∆ B ∆ (C ∆ D ∆ E) ∆ ... ∆ Y ∆ Z)
        '''
        from . import association
        return apply_association_thm(self, start_idx, length, association)

    @equality_prover('disassociated', 'disassociate')
    def disassociation(self, idx, **defaults_config):
        '''
        Deduce that this SymmetricDifference expression is equal to 
        a form in which the operand at index idx is no longer grouped
        together. For example, 

          (A ∆ B ∆ (C ∆ D ∆ E) ∆ ... ∆ Y ∆ Z).disassociation(2)

        would derive and return:

          |- (A ∆ B ∆ (C ∆ D ∆ E) ∆ ... ∆ Y ∆ Z)
             = (A ∆ B ∆ C ∆ D ∆ E ∆ ... ∆ Y ∆ Z)

        Multiple indices can be provided for multiple disassociations
        simultaneously, e.g. expr.disassociation(2, 3, 4).
        Notice that a disassociation() call can change the number of
        operands at the enclosing level (e.g. the example above took
        a 24-operand SymmetricDifference to a 26-operand
        SymmetricDifference, if we count the A, B, ..., Z literally).
        '''
        from . import disassociation
        return apply_disassociation_thm(self, idx, disassociation)

            