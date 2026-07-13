from proveit import (
        equality_prover, ExprTuple, Lambda, Literal, Operation,
        OperationOverInstances, single_or_composite_expression,
        TransRelUpdater, USE_DEFAULTS)
from proveit import i, x, y, f, A, P, Q, S


class UnionAll(OperationOverInstances):
    # operator of the UnionOfAll operation
    _operator_ = Literal(
        string_format='union_of_all',
        latex_format=r'\bigcup',
        theory=__file__)
    _init_argname_mapping_ = {'instance_element': 'instance_expr'}

    def __init__(self, instance_param_or_params, instance_element,
                 domain=None, *, domains=None, condition=None,
                 conditions=None, styles=None, _lambda_map=None):
        '''
        Create an expression representing the union of all
        instance_element for instance parameter(s) such that the conditions
        are satisfied:
        {instance_element | conditions}_{instance_param_or_params in S}
        '''
        OperationOverInstances.__init__(
            self, UnionAll._operator_, instance_param_or_params,
            instance_element, domain=domain, domains=domains,
            condition=condition, conditions=conditions,
            styles=styles, _lambda_map=_lambda_map)
        self.instance_element = self.instance_expr
        if hasattr(self, 'instance_param'):
            if not hasattr(self, 'domain'):
                raise ValueError("SetOfAll requires a domain")
        elif hasattr(self, 'instance_params'):
            if not hasattr(self, 'domains') or None in self.domains:
                raise ValueError("SetOfAll requires a domain(s)")
        else:
            assert False, ("Expecting either 'instance_param' or 'instance_params' "
                           "to be set")

    @equality_prover('shallow_simplified', 'shallow_simplify')
    def shallow_simplification(self, *, must_evaluate=False,
                               **defaults_config):
        '''
        Returns a proven simplification equation for this UnionAll
        expression assuming the operands have been simplified,
        according to the simplification directives as follows:

        * Reduce to the EmptySet any UnionAll with EmptySet as the
          index domain.

        * Reduce to the EmptySet any UnionAll with EmptySet as the
          instance expression.

        * Reduce to constant A and UnionAll with constant A as the
          instance expression.

        '''

        from proveit.logic import Equals
        from proveit.logic.sets import EmptySet

        # UnionAll with empty indexing domain: always the empty set
        if Equals(self.domain, EmptySet).readily_provable():
            from . import union_all_empty_domain
            _f_sub = Lambda(self.instance_param, self.instance_expr)
            _i_relabel = self.instance_param
            _inst = union_all_empty_domain.instantiate(
                    {f:_f_sub}, auto_simplify=False)
            _inst_relabeled = _inst.inner_expr().lhs.operand.relabeled(
                    {i:_i_relabel})
            return _inst_relabeled

        # UnionAll of EmptySet is the EmptySet
        if Equals(self.instance_expr, EmptySet).readily_provable():
            from . import union_all_of_empty
            _S_sub = self.domain
            _i_relabel = self.instance_param
            _inst = union_all_of_empty.instantiate(
                    {S:_S_sub}, auto_simplify=False)
            _inst_relabeled = _inst.inner_expr().lhs.operand.relabeled(
                    {i:_i_relabel})
            return _inst_relabeled

        # UnionAll of a constant A over non-empty domain is just A
        from proveit import free_vars
        from proveit.logic import NotEquals
        _instance_expr_vars = free_vars(self.instance_expr)
        _const_instance_expr = (
            len(_instance_expr_vars.intersection([self.instance_param])) == 0)
        if (_const_instance_expr and
            NotEquals(self.domain, EmptySet).readily_provable()):
            from . import union_all_constant
            _A_sub = self.instance_expr
            _S_sub = self.domain
            _i_relabel = self.instance_param
            _inst = union_all_constant.instantiate(
                    {A:_A_sub, S:_S_sub}, auto_simplify=False)
            _inst_relabeled = _inst.inner_expr().lhs.operand.relabeled(
                    {i:_i_relabel})
            return _inst_relabeled

        expr = self
        # for convenience in updating our equation, beginning with
        # self = self
        eq = TransRelUpdater(self)

        # OTHER stuff to be developed here.

        # otherwise ...
        return eq.relation # Might simply be self = self.
