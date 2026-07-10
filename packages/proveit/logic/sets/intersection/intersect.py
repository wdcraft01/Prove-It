from proveit import (
        equality_prover, Expression, ExprRange, Lambda, Literal,
        Operation, SimplificationDirectives, TransRelUpdater,
        USE_DEFAULTS)
from proveit import i, j, k, l, m, n, x, A, B, C, D, E, S
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

    def readily_factorable(self, factor):
        '''
        Return True iff 'factor' is readily factorable as a Union
        factor or as an Intersect factor from 'self' in an
        obvious manner. See the readily_intersect_factorable() and
        readily_union_factorable() for details.

        For example, the Intersect expression:

            A ∩ B ∩ (C ⋃ D) ∩ (E ∩ F)

        has factorable "Intersect factors" A, B, (C ⋃ D), (E ∩ F), E,
        and F. Notice that neither C nor D are factorable factors.

        Despite the borrowing of the "factor" terminology from the Add
        and Mult class methods, Intersect.readily_factorable() is
        not nearly so general as the Add and Mult versions, with a
        "factor" here limited to being a simple "factor" X such that
        self could theoretically be rewritten as X ∩ (remainder) or
        X ⋃ (remainder).
        '''

        return (self.readily_intersect_factorable(factor)
                or self.readily_union_factorable(factor))

    def readily_intersect_factorable(self, factor, multiplicity=1):
        '''
        Return True iff 'factor' is factorable from 'self' in an
        obvious manner as an intersection "factor" or operand, with at
        least the specified multiplicity. For an Intersect, a "factor"
        is readily factorable as an intersection factor if it appears
        as an operand in the Intersect expression or if it appears as
        an intersection factor of one of the Intersect operands.

        For example, the Intersect expression:

            A ∩ B ∩ (C ⋃ D) ∩ (E ∩ B)

        has factorable "intersection-factors" A, B, (C ⋃ D), (E ∩ B),
        and E. B has multiplicity 2. Notice that neither C nor D are
        intersection factors.

        Despite the borrowing of the "factor" terminology from the Add
        and Mult class methods, Intersect.readily_intersect_factorable()
        is not nearly so general as the Add and Mult versions, with a
        "factor" here limited to being an Intersect operand or an item
        X such that self = X n (remainder). See also the Intersect
        readily_union_factorable() for the dual factorability method.
        '''
        from collections import defaultdict

        # Perhaps the factor is itself the entire Intersect
        if self == factor:
            return True

        # Create the defaultdict for counting multiplicities
        _multiplicities = defaultdict(int)

        # Check to see if factor appears as an operand or as a
        # factor in one of the operands, with at least the specified
        # multiplicity.

        for _op in self.operands:
            if ((_op == factor) or
                (hasattr(_op, 'readily_intersect_factorable')
                 and _op.readily_intersect_factorable(factor))):

                _multiplicities[_op] += 1

                if _multiplicities[_op] == multiplicity:
                    return True
        
        return False

    def readily_union_factorable(self, factor, **defaults_config):
        '''
        Return True iff 'factor' is factorable from 'self' in an
        obvious manner as a Union "factor" or operand.
        For an Intersect, a "factor" is readily factorable as a
        Union factor if every operand of the Intersect is
        a Union and every such Union has 'factor' as a Union
        factor.

        For example, the Intersect expression:

            (A U B) n (B U C)

        has B as a factorable "union factor," and the expression
        can be re-written as [B U (A n C)].

        Despite the borrowing of the "factor" terminology from the Add
        and Mult class methods, Intersect.readily_union_factorable()
        is not nearly so general as the Add and Mult versions, with a
        "factor" here limited to being a Union operand appearing
        in every one of the Intersect operands. More complex factoring
        situations might require user pre-processing of the expression.
        See also the Intersect readily_intersect_factorable() method
        for the dual factorability method.
        '''

        # For the Intersect to even be possibly union-factorable,
        # each of the operands must be a Union
        from proveit.logic.sets import Union
        for _op in self.operands:
            if not isinstance(_op, Union):
                return False

        # Given that every operand is a Union, every such
        # Union must then have factor as a Union factor
        for _op in self.operands:
            if not _op.readily_union_factorable(factor):
                return False 

        return True

    def intersect_factorization(self, left_factors=None, right_factors=None,
                                group_factors=True, group_remainder=True,
                                **defaults_config):
        '''
        Derive and return an equality between self and the proven
        "factorization" of this Intersect expression produced by
        by pulling the factor(s) from this Intersect to the 
        "left" or "right" as "Intersect factors." For example, given
        self = A ∩ B ∩ ((C ∩ D) ⋃ (E ∩ C)) ∩ F, and calling

            self.intersect_factorization(
                left_factors = [B], right_factors = [C])

        we obtain

            self = B ∩ (A ∩ (D ⋃ E) ∩ F) ∩ C

        producing another Intersect expression on the rhs.

        If there are multiple occurrences, the first
        occurrence is used.  If group_factors is True, the factors are 
        grouped together as a sub-product.

        If group_remainder is True and there are multiple remaining
        operands, then these remaining operands are grouped.
        '''

        expr = self
        # A convenience for updating our developing equation
        eq = TransRelUpdater(expr)

        # No factors supplied for factorization?
        if (left_factors is None and right_factors is None):
            return eq.relation # self = self

        # Safely convert None values to empty lists
        left_factors = left_factors if left_factors is not None else []
        right_factors = right_factors if right_factors is not None else []
        all_factors = left_factors + right_factors

        # Check for bad factors
        _bad_factors = []
        for factor in set(all_factors):
            _multiplicity = all_factors.count(factor)
            if not self.readily_intersect_factorable(factor, _multiplicity):
                _bad_factors.append(factor)

        # If bad factors supplied, raise error and abandon
        if len(_bad_factors) > 0:
            raise ValueError(
                    "One or more bad factors supplied as arguments "
                    f"to Intersect.intersect_factorization(): {_bad_factors}")

        # And check if the multiplicity of supplied factors is valid
        # Perhaps modify the factorable() methods to check for multiplicity?

        # Factors are legitimate; derive the factored form

        if Intersect(*all_factors) == self:
            return eq.relation # self = self



        return all_factors



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
        Deduce that this Intersect expression is equal to an Intersect
        in which the operands at indices 0, 1, …, n-1 have been
        reordered as specified EITHER by the new_order list OR by the
        cycles list parameter. For example,

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

    @equality_prover('distributed', 'distribute')
    def distribution(self, idx=None, *, 
                     left_factors=None, right_factors=None, 
                     **defaults_config):
        r'''
        Modifies this Intersect expression by distributing through the
        operand at the given index, returning the equality between
        self and the new version. We keep the "factor" language,
        treating Intersect operands analogous to multiplicative factors.
        For example:

            (A ∩ (B1 U B2 U B3) ∩ C).distribution(1) returns:

            |- (A ∩ (B1 U B2 U B3) ∩ C) =
               (A ∩ B1 ∩ C) U (A ∩ B2 ∩ C) U (A ∩ B3 ∩ C)
        
        For more flexibility, 'left_factors' and 'right_factors'
        may be specified to indicate subsets of the factors to
        distribute on the left vs right. The 'left_factors' and 
        'right_factors' may be provided as indices instead.
        For example:

            (A ∩ B ∩ (C1 U C2) ∩ D).distribution(
                1, left_factors=[B], right_factors=[D]) returns:

            |- (A ∩ B ∩ (C1 U C2) ∩ D) =
               A ∩ ((B ∩ C1 ∩ D) U (B ∩ C2 ∩ D))

        If one of the left/right factors is specified but not the
        other, the empty set is used for the one that isn't specified.
        One can also use the left_factors and right_factors to force
        factors onto opposite sides from where they start.

        Currently, Intersect.distribute() works only to distribute
        Intersect operations through Union() or UnionAll() operations.
        '''
        from . import (distribute_through_difference,
                distribute_through_union, distribute_through_unionall)
        from proveit.logic.sets import Difference, Union, UnionAll
        if left_factors is not None or right_factors is not None:
            # Specific factors to be applied to the left and/or right
            # were provided.  So we'll reorder the factors and then
            # associate appropriately before distributing.
            if left_factors is None: left_factors = []
            if right_factors is None: right_factors = []
            # Convert from expressions to indices for the left and
            # right factors (exclude the 'idx').
            factor_to_index = {factor:_k for _k, factor 
                               in enumerate(self.operands) if _k != idx}
            left_factor_indices = list(left_factors)
            right_factor_indices = list(right_factors)
            for factor_indices in (left_factor_indices, right_factor_indices):
                for _k, factor in enumerate(factor_indices):
                    try:
                        if isinstance(factor, Expression):
                            factor_indices[_k] = factor_to_index.pop(factor)
                    except KeyError:
                        raise ValueError(
                                "The 'left_factors', %s, and 'right_factors'"
                                ", %s, do not all appear in %s"
                                %(self, left_factors, right_factors))
            # Permute the factors (i.e., operands) so the left factors
            # come just before the factor to distribute through and
            # the right factors come just after.
            factors = self.operands.entries
            num_factors = len(factors)
            special_indices = set(left_factor_indices).union(
                    right_factor_indices)
            before_indices = [_idx for _idx in range(idx) if
                              _idx not in special_indices]
            after_indices = [_idx for _idx in range(idx+1, num_factors) if
                              _idx not in special_indices]
            new_order = (before_indices + left_factor_indices + [idx] +
                         right_factor_indices + after_indices)
            eq = TransRelUpdater(self)
            expr = eq.update(self.permutation(new_order, auto_simplify=False))
            # Convert from indices to expressions.
            left_factors = [factors[_i] for _i in left_factor_indices]
            right_factors = [factors[_i] for _i in right_factor_indices]
            # Make the distribution.
            num_left_factors = len(left_factors)
            distribution = Intersect(*left_factors, factors[idx], 
                                *right_factors).distribution(
                                        num_left_factors)
            if len(before_indices)==len(after_indices)==0:
                # No factors are left out of the distribution.
                # For example: a b (c + d) e f = a f c b e + a f d b e
                eq.update(distribution)
                return eq.relation
            # Now associate to include from left factors to right
            # factors and simultaneously replace with the distribution.
            start = len(before_indices)
            length = num_left_factors + len(right_factors) + 1
            eq.update(expr.association(
                    start, length, replacements=[distribution],
                    auto_simplify=False))
            return eq.relation

        operand = self.operands[idx]
        _A_sub = self.operands[:idx]
        _C_sub = self.operands[idx + 1:]
        _l_sub = _A_sub.num_elements()
        _n_sub = _C_sub.num_elements()
        if isinstance(operand, Union):
            _B_sub = self.operands[idx].operands
            _m_sub = _B_sub.num_elements()
            return distribute_through_union.instantiate(
                {l:_l_sub, m:_m_sub, n:_n_sub, A:_A_sub, B:_B_sub, C:_C_sub})
        elif isinstance(operand, UnionAll):
            _lambda_param = operand.instance_param
            _S_sub   = operand.domain
            _B_sub = Lambda(_lambda_param, operand.operand.body.value)
            return distribute_through_unionall.instantiate(
                {l:_l_sub, n:_n_sub, S:_S_sub, A:_A_sub, B:_B_sub, C:_C_sub})
        elif isinstance(operand, Difference):
            _D_sub = operand.operands[0]
            _E_sub = operand.operands[1]
            return distribute_through_difference.instantiate(
                {l:_l_sub, n:_n_sub, A:_A_sub, C:_C_sub, D:_D_sub, E:_E_sub})
        else:
            raise NotImplementedError(
                "Unsupported operand type to distribute over: " +
                str(operand.__class__))
