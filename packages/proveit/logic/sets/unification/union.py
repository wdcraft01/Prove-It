from proveit import (
        defaults, equality_prover, Expression, ExprRange, ExprTuple,
        Lambda, Literal, Operation, USE_DEFAULTS, relation_prover,
        SimplificationDirectives, TransRelUpdater)
from proveit import i, j, k, l, m, n, A, B, C, S, x
from proveit.abstract_algebra.generic_methods import (
        apply_association_thm, apply_commutation_thm,
        apply_disassociation_thm, generic_permutation, group_commutation,
        sorting_and_combining_like_operands)


class Union(Operation):
    # operator of the Intersect operation
    _operator_ = Literal(
        string_format='union',
        latex_format=r'\cup',
        theory=__file__)

    _simplification_directives_ = SimplificationDirectives(
            ungroup=True)

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

    @equality_prover('shallow_simplified', 'shallow_simplify')
    def shallow_simplification(self, *, must_evaluate=False,
                               **defaults_config):
        '''
        Returns a proven simplification equation for this Union
        expression assuming the operands have been simplified
        according to the simplification directives as follows:

        If ungroup is True (the default), dissociate nested Unions.
        
        If sorting is required, sort operands according to order_key_fn
        where the key is simply the operand itself.

        Eliminate any EmptySet operands (assuming this leaves at
        least one non-EmptySet operand), since A U EmptySet = A,
        and eliminate repeating operands, since A U A = A (eliminating
        EmptySet operands and repeated operands is similar to 
        eliminating multiplication factors of 1 in the Mult class).

        Notice that, unlike multiplication, Union has no general "zero"
        factor or "absorbing factor" in the Prove-It system. Such a
        zero factor would be equivalent to a universal set, which is
        not allowed.
        '''

        # from proveit.logic.sets import EmptySet
        from . import empty_union_eval, unary_union_reduction

        # Empty Union U()
        if self.operands.num_entries() == 0:
            # empty Union is equal to the EmptySet
            return empty_union_eval

        # Unary Union U(A)
        if self.operands.is_single():
            # Union(A) is equal to A
            _A_sub = self.operands[0]
            return unary_union_reduction.instantiate({A:_A_sub})

        expr = self
        # for convenience in updating our equation, beginning with
        # self = self
        eq = TransRelUpdater(self)

        # Ungroup the expression (disassociate nested Unions).
        if Union._simplification_directives_.ungroup:
            idx = 0
            length = expr.operands.num_entries() - 1
            while idx < length:
                # loop through all operands
                if isinstance(expr.operands[idx], Union):
                    # if it is grouped, ungroup it
                    expr = eq.update(expr.disassociation(
                            idx, preserve_all=True))
                else:
                    idx += 1
                length = expr.operands.num_entries()

        # likeness of operands is simply equality of operands ---
        # i.e. two operands are "alike" if they are equal
        likeness_key_fn = lambda operand : operand

        # Combine like operands.
        expr = eq.update(sorting_and_combining_like_operands(
                    expr, order_key_fn=lambda likeness_key : 0, 
                    likeness_key_fn=likeness_key_fn,
                    preserve_likeness_keys=True, auto_simplify=True))

        if isinstance(expr, Union):
            # Remove any remaining EmptySets
            expr = eq.update(expr.empty_set_eliminations())

        if not isinstance(expr, Union):
            # Simplified to a non-Union. We're done.
            return eq.relation

        # othewise ...
        return eq.relation # Might simply be self = self.

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

    @equality_prover('eliminated_empty_sets', 'eliminate_empty_sets')
    def empty_set_eliminations(self, **defaults_config):
        '''
        Equality prover method that derives a simplification in which
        EmptySet operands are eliminated. For example,

            Union(A, EmptySet, B, EmptySet, C, EmptySet).
            empty_set_eliminations()

        derives and returns: |- (A U ∅ U B U ∅ U C U ∅) = (A U B U C).
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
                if not isinstance(expr, Union):
                    # can't do an elimination if reduced to a single term.
                    break

        return eq.relation

    @equality_prover('eliminated_empty_set', 'eliminate_empty_set')
    def empty_set_elimination(self, idx, **defaults_config):
        '''
        Equality prover method that derives a simplification in which
        a single EmptySet operand, at the given index, is eliminated.
        For example, Union(A, B, EmptySet, C).empty_set_elimination(2)
        would return:
                       |- (A U B U ∅ U C) = (A U B U C)
        '''
        from proveit.logic.sets import EmptySet
        from . import (union_with_empty_left, union_with_empty_right,
                       union_with_empty)

        if self.operands[idx] != EmptySet: # might need isinstance?
            raise ValueError(
                f"Operand at the provided index idx = {idx} expected "
                f"to be an EmptySet for {self}")

        if self.operands.is_double():
            if idx == 0:
                return union_with_empty_left.instantiate({A: self.operands[1]})
            else:
                return union_with_empty_right.instantiate({A: self.operands[0]})
        _A_sub = self.operands[:idx]
        _B_sub = self.operands[idx + 1:]
        _m_sub = _A_sub.num_elements()
        _n_sub = _B_sub.num_elements()
        return union_with_empty.instantiate(
                {m: _m_sub, n: _n_sub, A: _A_sub, B: _B_sub})

    @equality_prover('consolidated_to_unionall', 'consolidate_to_unionall')
    def consolidation_to_unionall(self, instance_param=None, **defaults_config):
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

    @equality_prover('combined_operands', 'combine_operands')
    def combining_operands(self, start_idx=None, end_idx=None,
                           **defaults_config):
        '''
        combining_operands() is called from generic_methods.py,
        providing a formula/algorithm for combining operands.
        For a Union, combining operands essentially means redundancy
        reduction, where A U A can be reduced to just A.
        Notice that "like terms" here means identical terms, and
        combining like terms amounts to eliminating redundant terms.
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
            # [U]() = EmptySet
            from . import empty_union_eval
            return empty_union_eval

        if self.operands.num_entries()==1 and (
                isinstance(self.operands[0], ExprRange) and 
                self.operands[0].is_parameter_independent):
            # A U A U ... U A = A
            operand_range = self.operands[0]
            _A_sub = operand_range.body
            _n_sub = self.operands.num_elements()
            replacements = list(defaults.replacements)
            if operand_range.start_index != one:
                # Transform from as ExprRange that start at 1.
                replacements.append(operand_range.reduction().derive_reversed())
            from . import redundant_union_range
            inst = redundant_union_range.instantiate(
                    {n:_n_sub, A:_A_sub}, replacements=replacements)
            return inst

        operands = list(self.operands.entries)

        # If we try to combine more than 2 operands, we run into
        # trouble because it's problematic to prove that the ExprRange
        # produced by the underlying theorem is equal to an equivalent
        # ExprTuple. Instead, we try to recursively reduce the number
        # of identical operands being considered by repeatedly dealing
        # with the operands pair-wise. 
        _num_operands = self.operands.num_elements().as_int()
        # It would be nice to do this via the TransRelUpdater(),
        # but for now we do the work ourselves.
        main_eq = Equals(self, self).prove(auto_simplify=False)
        while _num_operands > 2:
            # Successively take a sub-group of two operands
            # and reduce it to a single operand.

            # Associate the operands intended for combination.
            # Warning: 2nd arg of association() is length not index.
            main_eq = main_eq.apply_transitivity(main_eq.rhs.
                    association(0, 2, auto_simplify=False))
            # NOTE: it's possible that Union.association() and keeping
            # auto_simplify would take care of each Union(A, A)=A
            # transformation all by itself, which would be cool.
            # Something to try in the future.

            # Isolate the targeted factors and combine them as desired
            # using call to this same combining_operands() method
            inner_combination = (
                    main_eq.rhs.operands[0].combining_operands())
            main_eq = inner_combination.sub_right_side_into(main_eq, auto_simplify=False)
            if isinstance(main_eq.rhs, Union):
                _num_operands = main_eq.rhs.operands.num_elements().as_int()
            else:
                return main_eq

        # try instantiating the redundant_union_range
        if _num_operands == 2:
            from . import redundant_union_range
            _A_sub = main_eq.rhs.operands[0]
            _n_sub = main_eq.rhs.operands.num_elements()
            from proveit import safe_dummy_var
            replacements = []
            replacements.append(
                Equals(ExprTuple(ExprRange(safe_dummy_var(), _A_sub, one, _n_sub)),
                       main_eq.rhs.operands).prove())
            inst = redundant_union_range.instantiate(
                        {n:_n_sub, A:_A_sub}, replacements=replacements, auto_simplify=False)
            return main_eq.apply_transitivity(inst)

        return Equals(self, self).conclude_via_reflexivity()

    def readily_factorable(self, factor):
        '''
        Return True iff 'factor' is readily factorable as a Union
        factor or as an Intersect factor from 'self' in an
        obvious manner. See the readily_intersect_factorable() and
        readily_union_factorable() for details.

        For example, the Union expression:

            A ⋃ B ⋃ (C ∩ D) ⋃ (E ⋃ F)

        has factorable "Union factors" A, B, (C ∩ D), (E ⋃ F), E,
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

    def readily_intersect_factorable(self, factor, **defaults_config):
        '''
        Return True iff 'factor' is factorable from 'self' in an
        obvious manner as an intersection "factor" or operand.
        For a Union, a "factor" is readily factorable as an
        intersection factor if the every operand of the Union is
        an Intersect and every such Intersect has 'factor' as an
        Intersect factor.

        For example, the Union expression:

            (A n B) U (B n C)

        has B as a factorable intersect "factor," and the expression
        can be re-written as [B n (A U C)].

        Despite the borrowing of the "factor" terminology from the Add
        and Mult class methods, Union.readily_intersect_factorable()
        is not nearly so general as the Add and Mult versions, with a
        "factor" here limited to being an Intersect operand appearing
        in every one of the Union operands. More complex factoring
        situations might require user pre-processing of the expression.
        See also the Union readily_union_factorable() for the dual
        factorability method.
        '''

        # For the Union to even be possibly intersect factorable,
        # each of the operands must be an Intersect
        from proveit.logic.sets import Intersect
        for _op in self.operands:
            if not isinstance(_op, Intersect):
                return False

        # Given that every operand is an Intersect, every such
        # Intersect must then have factor as an Intersect factor
        for _op in self.operands:
            if not _op.readily_intersect_factorable(factor):
                return False 

        return True

    def readily_union_factorable(self, factor):
        '''
        Return True iff 'factor' is factorable from 'self' in an
        obvious manner as a "union factor" or operand.
        For a Union, a "factor" is readily factorable as a
        "union factor" if it appears as an operand in the
        Union expression or if it appears as a Union factor
        of one of the Union operands.

        For example, the Union expression:

            A ⋃ B ⋃ (C ∩ D) ⋃ (E ⋃ F)

        has factorable "union factors" A, B, (C ∩ D), (E ⋃ F),
        E, and F. Notice that neither C nor D are union factors.

        Despite the borrowing of the "factor" terminology from the Add
        and Mult class methods, Union.readily_union_factorable() is not
        nearly so general as the Add and Mult readily_factorable()
        methods, with a "factor" here limited to being a Union
        operand or an item X such that self = X ⋃ (remainder).
        More complex factoring situations might require user pre-
        processing of the expression. See also the Union
        readily_intersect_factorable() for the dualfactorability method.
        '''

        # Perhaps the factor is itself the entire Union
        if self == factor:
            return True

        # Check to see if factor appears as an operand or as a
        # "union factor" in one of the operands
        for _op in self.operands:
            if ((_op == factor) or
                (hasattr(_op, 'readily_union_factorable')
                 and _op.readily_union_factorable(factor))):

                return True
        
        return False

    @equality_prover('commuted', 'commute')
    def commutation(self, init_idx=None, final_idx=None, **defaults_config):
        '''
        Deduce that this Union expression is equal to a form in which
        the operand at index init_idx has been moved to index final_idx.
        For example, (a U b U ... U y U z).commutation(1, -2) will
        produce: |-  (a U b U ... U y U z) = (a U ... U y U b U z).
        '''
        from . import commutation, leftward_commutation, rightward_commutation
        return apply_commutation_thm(
            self, init_idx, final_idx, commutation,
            leftward_commutation, rightward_commutation)

    @equality_prover('group_commuted', 'group_commute')
    def group_commutation(self, init_idx, final_idx, length,
                          disassociate=True, **defaults_config):
        '''
        Deduce that this Union expression is equal to a form in which
        the operands at indices [init_idx, init_idx+length) have been
        moved to [final_idx, final_idx+length).
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
        Deduce that this Union expression is equal to a form in which
        the operand at index init_idx has been moved to final_idx.
        For example, (A U B U ... U Y U Z).permutation_move(1, -2) will
        produce: |- (A U B U ... U Y U Z) = (A U ... U Y U B U Z),
        moving operand B from position index 1 to position index -2.
        For the Union class, this method just immediately calls the
        Union.commutation() method; we keep the permutation_move()
        method because it is used by the permutations machinery
        available in abstract_algebra/generic_methods.py.
        '''
        return self.commutation(init_idx=init_idx, final_idx=final_idx)

    @equality_prover('permuted', 'permute')
    def permutation(self, new_order=None, cycles=None, **defaults_config):
        '''
        Deduce that this Union expression is equal to a Union in which
        the operands at indices 0, 1, …, n-1 have been reordered as
        specified EITHER by the new_order list OR by the cycles list
        parameter. For example,

            (A U B U C U D).permutation(new_order=[0, 2, 3, 1])

        and (A U B U C U D).permutation(cycles=[(1, 2, 3)])

        would both return ⊢ (A U B U C U D) = (A U C U D U B).
        '''
        return generic_permutation(self, new_order, cycles)

    @equality_prover('associated', 'associate')
    def association(self, start_idx, length, **defaults_config):
        '''
        Deduce that this expression is equal to a form in which
        operands in the range [start_idx, start_idx+length) are
        grouped together. For example,

            (A U B U C U D U E U ... U Y U Z).association(2, 3)

        would derive and return:

            |- (A U B U C U D U E U ... U Y U Z)
               = (A U B U (C U D U E) U ... U Y U Z)
        '''
        from . import association
        return apply_association_thm(self, start_idx, length, association)

    @equality_prover('disassociated', 'disassociate')
    def disassociation(self, idx, **defaults_config):
        '''
        Deduce that this expression is equal to a form in which the
        operand at index idx is no longer grouped together.
        For example,

            (A U B U (C U D U E) U ... U Y U Z).disassociation(2)

        would derive and return:

            |- (A U B U (C U D U E) U ... U Y U Z)
               = (A U B U C U D U E U ... U Y U Z)
        
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
        Modifies this Union expression by distributing through the
        operand at the given index, returning the equality between
        self and the new version. We keep the "factor" language,
        treating Union operands analogous to multiplicative factors.
        For example:

            (A U (B1 ∩ B2 ∩ B3) U C).distribution(1) returns:

            |- (A U (B1 ∩ B2 ∩ B3) U C) =
               (A U B1 U C) ∩ (A U B2 U C) ∩ (A U B3 U C)
        
        For more flexibility, 'left_factors' and 'right_factors'
        may be specified to indicate subsets of the factors to
        distribute on the left vs right. The 'left_factors' and 
        'right_factors' may be provided as indices instead.
        For example:

            (A U B U (C1 ∩ C2) U D).distribution(
                1, left_factors=[B], right_factors=[D]) returns:

            |- (A U B U (C1 ∩ C2) U D) =
               A U ((B U C1 U D) ∩ (B U C2 U D))

        If one of the left/right factors is specified but not the
        other, the empty set is used for the one that isn't specified.
        One can also use the left_factors and right_factors to force
        factors onto opposite sides from where they start.

        Currently, Union.distribute() works only to distribute Union
        operations through Intersect() or IntersectAll() operations.
        '''
        from . import (distribute_through_intersection,
                distribute_through_intersectall)
        from proveit.logic.sets import Intersect, IntersectAll
        from proveit.numbers.division import prod_of_fracs
        from proveit.numbers import Neg, Abs, Div, Sum
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
            distribution = Union(*left_factors, factors[idx], 
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
        if isinstance(operand, Intersect):
            _B_sub = self.operands[idx].operands
            _m_sub = _B_sub.num_elements()
            return distribute_through_intersection.instantiate(
                {l:_l_sub, m:_m_sub, n:_n_sub, A:_A_sub, B:_B_sub, C:_C_sub})
        elif isinstance(operand, IntersectAll):
            _lambda_param = operand.instance_param
            _S_sub   = operand.domain
            _B_sub = Lambda(_lambda_param, operand.operand.body.value)
            return distribute_through_intersectall.instantiate(
                {l:_l_sub, n:_n_sub, S:_S_sub, A:_A_sub, B:_B_sub, C:_C_sub})
        else:
            raise NotImplementedError(
                "Unsupported operand type to distribute over: " +
                str(operand.__class__))
            