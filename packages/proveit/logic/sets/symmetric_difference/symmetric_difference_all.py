from proveit import (
        A, S, equality_prover, ExprTuple, Function, Lambda, Literal,
        Operation, OperationOverInstances, single_or_composite_expression,
        TransRelUpdater, USE_DEFAULTS)
from proveit import i, x, y, f, A, P, Q, S


class SymmetricDifferenceAll(OperationOverInstances):
    '''
    SymmetricDifferenceAll(A(i), domain) represents the symmetric
    difference of the operand sets A(i) for i in domain, displayed
    symbolically as:

        ∆_{i in domain}(A(i))

    and representing the symmetric difference A(j) ∆ A(k) ∆ ... ∆ A(n)
    for j, k, ..., n in domain.

    The symmetric difference of two sets A and B, represented by
    SymmetricDifference(A,B) and displayed as A ∆ B, is the set of
    elements that are in set A or in set B but not in both. In the
    more general case, A1 ∆ A2 ∆ ... ∆ An is the set of elements that
    appear in exactly an odd number of the operand sets A1,...,An.

    The SymmetricDifferenceAll class is established in addition to the
    standard SymmetricDifference class to offer more expressiveness
    and under some circumstances easier instantiation when utilized
    in an axiom or theorem.
    '''

    # operator of the SymmetricDifferenceAll operation
    _operator_ = Literal(
        string_format='sym_diff_of_all',
        latex_format=r'\mathop\bigtriangleup',
        theory=__file__)
    _init_argname_mapping_ = {'instance_element': 'instance_expr'}

    def __init__(self, instance_param_or_params, instance_element,
                 domain=None, *, domains=None, condition=None,
                 conditions=None, styles=None, _lambda_map=None):
        '''
        Create an expression representing the symmetric difference of
        all cases of the instance_element for instance parameter(s)
        such that the conditions are satisfied.
        '''
        OperationOverInstances.__init__(
            self, SymmetricDifferenceAll._operator_,
            instance_param_or_params,
            instance_element, domain=domain, domains=domains,
            condition=condition, conditions=conditions,
            styles=styles, _lambda_map=_lambda_map)
        self.instance_element = self.instance_expr
        if hasattr(self, 'instance_param'):
            if not hasattr(self, 'domain'):
                raise ValueError(
                    "SymmetricDifferenceAll requires a domain")
        elif hasattr(self, 'instance_params'):
            if not hasattr(self, 'domains') or None in self.domains:
                raise ValueError(
                    "SymmetricDifferenceAll requires a domain "
                    "or domains. ")
        else:
            assert False, (
                "Expecting either 'instance_param' or "
                "'instance_params' to be set")

    @equality_prover('shallow_simplified', 'shallow_simplify')
    def shallow_simplification(self, *, must_evaluate=False,
                               **defaults_config):
        '''
        Returns a proven simplification equation for this
        SymmetricDifferenceAll expression, assuming the operands have
        been simplified, according to the simplification directives
        as follows:

        * If the index set is empty, so is the symmetric difference
          expression.

        '''
        from proveit.logic import Equals
        from proveit.logic.sets import EmptySet

        # Index set is empty
        if hasattr(self, 'domain'):
            if Equals(self.domain, EmptySet).readily_provable():
                from . import sym_diff_all_def_base
                if isinstance(self.instance_element, Function):
                    _A_sub = self.instance_element.operator
                else:
                    _A_sub = self.instance_element
                _S_sub = self.domain
                return sym_diff_all_def_base.instantiate(
                        {A:_A_sub, S:_S_sub}).derive_consequent()

        # # Empty SymmetricDifference, ∆()
        # if self.operands.num_entries() == 0:
        #     from . import empty_sym_diff_eval
        #     # SymmetricDifference() = EmptySet
        #     return empty_sym_diff_eval

        # # Unary SymmetricDifference, ∆(A)
        # if self.operands.is_single():
        #     # ∆(A) = A
        #     from . import unary_sym_diff_reduction
        #     _A_sub = self.operands[0]
        #     return unary_sym_diff_reduction.instantiate({A:_A_sub})

        expr = self
        # for convenience in updating our equation, begining with
        # self = self
        eq = TransRelUpdater(self)

        # Ungroup the expression (disassociate nested ∆s)
        # if SymmetricDifference._simplification_directives_.ungroup:
        #     idx = 0
        #     length = expr.operands.num_entries() - 1
        #     while idx < length:
        #         # loop through all operands
        #         if isinstance(expr.operands[idx], SymmetricDifference):
        #             # if it is grouped, ungroup it
        #             expr = eq.update(expr.disassociation(
        #                         idx, preserve_all=True))
        #         else:
        #             idx += 1
        #         length = expr.operands.num_entries()

        # Likeness of operands is simply equality of operands ---
        # i.e., two operands are "alike" if they are equal
        # likeness_key_fn = lambda operand : operand

        # Combine like operands: A ∆ A = EmptySet
        # expr = eq.update(sorting_and_combining_like_operands(
        #         expr, order_key_fn=lambda likeness_key : 0,
        #         likeness_key_fn=likeness_key_fn,
        #         preserve_likeness_keys=True, auto_simplify=True))

        # if isinstance(expr, SymmetricDifference):
        #     # Remove any remaining EmptySets
        #     expr = eq.update(expr.empty_set_eliminations())

        # if not isinstance(expr, SymmetricDifference):
        #     # Simplified to something other than a SymmetricDifference.
        #     # We're done here.
        #     return eq.relation

        return eq.relation # Might simply be self = self.
