from proveit import (
        b, f, n, s, A, B, G, equality_prover, Function, Literal,
        NamedExprs, Operation, prover, relation_prover, TransRelUpdater)
from proveit.logic import InSet, SetMembership, SetNonmembership
from proveit.logic.sets import Disjoint
from proveit.numbers import Complex, Integer, Natural, Real


class BufiloSetsLiteral(Literal):
    '''
    BufiloSetsLiteral() (formatted as BUFS in outputs) represents
    the set of possible BUFILOs (standing for Bad Undetectable
    Fault-Induced Logical Operator) across a surface code. A BUFILO
    is itself a set of faults, the combination of which produce the
    equivalent of a logical operator L. The sets of interest can
    eventually be parameterized to specify a logical operator
    L, the logical operator L_{perp} with which it anti-commutes,
    and/or the specific QEC system of interest.

    'BufiloSets' is then defined in the QEC2 common notebook as
    BufiloSets = BufiloSetsLiteral().
    '''

    # the literal string for representing the BufiloSets
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='BUFS', 
                         latex_format=r'\textsc{bufs}',
                         styles=styles)

    def membership_object(self, element):
        from . import BufiloSetsMembership
        return BufiloSetsMembership(element, self)


class BufiloSetsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    BUFILOs.

    UNDER CONSTRUCTION, with the code below borrowed from the
    logic/sets/Union class and serving as a placeholder.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    # def side_effects(self, judgment):
    #     '''
    #     TBA.
    #     '''
    #     yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        From [b in BUFS], deduce and return the equality

            [b in BUFS] = 
            [b in ERRS AND H(b)=EmptySet AND A_{l}(b)=1]

        where H is the CheckFunction and A is the ActionFunction.
        '''

        from . import bufs_membership_def
        _b_sub = self.element
        return bufs_membership_def.instantiate(
                {b: _b_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From [b in BUFS], return the expression (NOT a Judgment):

            [b in ERRS AND H(b)=EmptySet AND A_{l}(b)=1]

        where H is the CheckFunction and A is the ActionFunction.
        '''
        from proveit.logic import And, Equals
        from proveit.logic.sets import EmptySet
        from proveit.numbers import one
        from . import _ell, ActionFunction, CheckFunction, Errors
        element = self.element
        return And(InSet(element, Errors),
                   Equals(CheckFunction(element), EmptySet),
                   Equals(ActionFunction(_ell, element), one))

    @prover
    def unfold(self, **defaults_config):
        '''
        From [b in BUFS], deduce and return the Judgment:

            [b in ERRS AND H(b)=EmptySet AND A_{l}(b)=1]

        where H is the CheckFunction and A is the ActionFunction.
        '''
        from . import bufs_membership_unfolding
        _b_sub = self.element
        return bufs_membership_unfolding.instantiate(
            {b: _b_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        From [b in BUFS], and knowing or assuming that 

            [b in ERRS AND H(b)=EmptySet AND A_{l}(b)=1]

        where H is the CheckFunction and A is the ActionFunction,
        derive and return self (as a Judgment).
        '''
        from . import bufs_membership_folding
        _b_sub = self.element
        return bufs_membership_folding.instantiate({b: _b_sub})


class IrreducibleBufiloSetsLiteral(Literal):
    '''
    IrreducibleBufiloSetsLiteral() (formatted as iBUFS in outputs)
    represents the set of possible irreducible BUFILOs (standing for
    Bad Undetectable Fault-Induced Logical Operator) across a surface
    code. A BUFILO is itself a set of faults, the combination of which
    produce the equivalent of a logical operator L. An irreducible
    BUFILO is a BUFILO that does not properly contain another BUFILO
    as a subset and does not contain any homologically trivial loops.
    
    The sets of interest can eventually be parameterized to specify a
    specific logical operator L, the logical operator L_{perp} with
    which it anti-commutes, and/or the specific QEC system of interest.

    'IrreducibleBufiloSets' is then defined in the QEC2 common
    notebook as IrreducibleBufiloSets = IrreducibleBufiloSetsLiteral().
    '''

    # the literal string for representing the IrreducibleBufiloSets
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='iBUFS', 
                         latex_format=r'i\textsc{bufs}',
                         styles=styles)

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Deduce and return 
            iBUFS = 
            [b | b in BUFS
                 AND (NotExists(b' in BUFS) s.t. b' subset b].

        That is, iBUFS is the set of BUFS each of which has no BUF
        as a proper subset.
        '''

        from . import irreducible_bufs_def
        return irreducible_bufs_def


class BufiloSequencesLiteral(Literal):
    '''
    BufiloSequencesLiteral() (formatted as F_{l,w} in outputs)
    represents a restricted set of fault sequences, each sequence
    having the following properties:

      * its weight is less than or equal to w_{BUF}
      * the first fault in the sequence anti-commutes with the
        logical operator l (i.e., A_{l} f_{1} = 1)
      * consider as a _set_, the sequence is equivalent to an
        l^{perp}-BUFILO (i.e., letting f = {f1, f2, ..., fn}, we
        have H f = ZeroVector while A_{l} f = 1).

    See BufiloSetsLiteral class above for further description of the
    related BUFILO sets.

    These sequences could eventually be parameterized to specify a
    specific logical operator l with which the sequences anti-commute,
    and/or the specific QEC system of interest.

    'BufiloSequences' is then defined in the QEC2 common notebook as
    BufiloSequences = BufiloSequencesLiteral().
    '''

    # the literal string for representing the BufiloSequences
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='F_{l w_BUF}', 
            latex_format=r'\mathcal{F}_{\ell w_{\textsc{buf}}}^{\text{seq}}',
            styles=styles)


class MalignantSetsLiteral(Literal):
    '''
    MalignantSetsLiteral() (formatted as MALS in outputs) represents
    the set of possible "malignant sets." A malignant set is a specific
    set of faults that causes a quantum error correction system to 
    suffer a logical failure. In Beverland's notation, a malignant
    set e is a set of faults such that H(e+c)=0 while A(e+c)≠0, where
    H is the check matrix, A is the action matrix, and c = C(sigma)
    is the correction provided by the decoding algorithm C.

    As in the case of BUFILO sets, the malignant sets of interest can
    eventually be parameterized to specify a QEC of interest.
    '''

    # The literal string for representing the malignant sets
    def __init__(self, *, styles=None):
        Literal.__init__(self, string_format='MALS', 
                         latex_format=r'\textsc{mals}',
                         styles=styles)


class Weight(Function):
    '''
    Weight(e), appearing as w(e) in outputs, represents the weight
    of error e, where error e consists of a set of faults. When
    e is represented as a vector over the 2-element finite field F,
    the weight is equivalent to the Hamming weight of the vector e.
    '''

    # the literal operator for the Weight operation
    _operator_ = Literal(
            string_format='w',
            latex_format=r'w\!', theory=__file__)

    def __init__(self, e, *, styles=None):
        '''
        Create Weight(e), the weight of error or fault set 'e'.
        '''
        Function.__init__(
                self, Weight._operator_, e, styles=styles)

    @equality_prover('shallow_simplified', 'shallow_simplify')
    def shallow_simplification(self, *, must_evaluate=False,
                               **defaults_config):
        '''
        Returns a proven simplification equation for this Weight
        expression assuming its operand has been simplified.
        
        Originally implemented to handles the following Weight
        expression "simplification":

             1. w(A U B) = w(A) + w(B) for Disjoint(A, B)

        but later decided not to make that an automatic simplification,
        and created a separate distribution_over_union() method instead.

        Left the shell of the shallow_simplification() method here for
        future development.

        '''
        expr = self
        # for convenience in updating our equation,
        # beginning with self = self
        eq = TransRelUpdater(expr)

        # (1) w(A U B) = w(A) + w(B) for Disjoint(A,B)
        # from proveit.logic.sets import Union
        # if isinstance(self.operand, Union):
        #     from proveit.logic.sets import Disjoint
        #     if Disjoint(*self.operand.operands).readily_provable():
        #         from proveit.physics.quantum.QEC2 import weight_additivity
        #         _A_sub = expr.operand.operands
        #         _n_sub = _A_sub.num_elements()
        #         expr = eq.update(weight_additivity.instantiate(
        #                     {n:_n_sub, A:_A_sub}))

        return eq.relation # Might be just [self = self]

    @equality_prover('distributed_over_union', 'distribute_over_union')
    def distribution_over_union(self, **defaults_config):
        '''
        Distribute a Weight(A U B) expression across its (binary)
        Union operand, returning an equality between the original
        expression and a sum of weights, as follows:

            1. The general case:
               w(A U B) = w(A) + w(B) - w(A n B)

            2. If Disjoint(A, B):
               w(A U B) = w(A) + w(B)
        
        Currently implemented only for the binary case, but could
        be generalized.
        '''
        from proveit.logic.sets import Union
        if (not isinstance(self.operand, Union)
            or not self.operand.operands.is_double()):
            raise ValueError(
                f"Weight.distribution_over_union() implemented only for "
                f"Weight() operation on a binary Union expression, but "
                f"received the expression: {self}.")

        _A_sub = self.operand.operands[0]
        _B_sub = self.operand.operands[1]
        if Disjoint(_A_sub, _B_sub).readily_provable():
            from proveit.physics.quantum.QEC2 import (
                    binary_disjoint_weight_additivity)
            return binary_disjoint_weight_additivity.instantiate(
                    {A:_A_sub, B:_B_sub})

        # Else return the more general case
        from proveit.physics.quantum.QEC2 import binary_weight_additivity
        return binary_weight_additivity.instantiate(
                {A:_A_sub, B:_B_sub})

        # raise NotImplementedError(
        #     f"Weight.distribution_over_union() not yet implemented for "
        #     f"the case of {self}. ")



    @relation_prover
    def deduce_in_number_set(self, number_set, **defaults_config):
        '''
        Attempt to prove that the given Weight expression is in the
        given number set number_set using the basic weight-defining
        set theorem. Weight(e) is always a Natural, and thus Weight(e)
        is also an Integer, a Real, and a Complex.
        '''
        
        if number_set in {Complex, Integer, Natural, Real}:
            from proveit.physics.quantum.QEC2 import weight_in_natural
            _A_sub = self.operand
            weight_in_natural_inst = weight_in_natural.instantiate({A:_A_sub})
            if number_set == Natural:
                return weight_in_natural_inst
            return InSet(self, number_set).prove()

        raise NotImplementedError(
            f"'Weight.deduce_in_number_set()' on {self} not "
            f"implemented for the {number_set} set. Remember that "
            f"Weight(e) is always a Natural number.")

    def readily_provable_number_set(self):
        '''
        Return the most restrictive number set we can readily
        prove contains the evaluation of this Weight operation.
        Generally, the most restrictive set is the set of Natural,
        but for an operand that is provably not the EmptySet, the
        most restrictive set would be the set NaturalPos.
        '''
        from proveit.logic import NotEquals
        from proveit.logic.sets import EmptySet
        from proveit.numbers import Natural, NaturalPos
        if NotEquals(self.operand, EmptySet).readily_provable():
            return NaturalPos
        return Natural


class FaultsLiteral(Literal):
    '''
    FaultsLiteral() (formatted as FAULTS in outputs) represents the
    set of possible faults across a QEC system. An error e consists
    of a set of such faults, and as described elsewhere, a BUFILO is
    a special set of such faults.

    See BufiloSetsLiteral class above for further description of the
    related BUFILO sets.

    'Faults' is then defined in the QEC2 common notebook as
    Faults = FaultsLiteral().
    '''

    # the literal string for representing the set of Faults
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='FAULTS', 
            latex_format=r'\textsc{faults}',
            styles=styles)


class ErrorsLiteral(Literal):
    '''
    ErrorsLiteral() (formatted as ERRS in outputs) represents the set
    of all possible errors across a QEC system, with an error simply
    being a set of faults.

    'Errors' is then defined in the QEC2 common notebook as
    Errors = ErrorsLiteral().

    The Errors class is a convenience to help facilitate expressiveness.
    One might use [e in Errors], for example, but often one could
    instead simply directly consider a set {f1, f2, ..., fn} of faults.
    '''

    # the literal string for representing the set of Errors
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='ERRS', 
            latex_format=r'\textsc{errs}',
            styles=styles)


class SyndromesLiteral(Literal):
    '''
    SyndromesLiteral() (formatted as mathcal{S} in outputs) represents
    the set of all possible syndromes, equivalent to the power set of
    the set of all detectors.
    This might eventually need to be generalized to a function 
    parameterized with an operator type, etc.
    '''
    # the literal string for representing the set of Syndromes
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='Syndromes', 
            latex_format=r'\mathcal{S}',
            styles=styles)


class DetectorsLiteral(Literal):
    '''
    DetectorsLiteral() (formatted as mathcal{D} in outputs) represents
    the set of all possible detectors.
    This might eventually need to be generalized to a function 
    parameterized with an operator type, etc.
    '''

    # the literal string for representing the set of Detectors
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='Detectors', 
            latex_format=r'\mathcal{D}',
            styles=styles)


class StatesLiteral(Literal):
    '''
    StatesLiteral() (formatted as S_{l} in outputs) represents the set
    of all possible augmented syndrome states of the form

        S_{l}(e) = (H e, A_{l} e)

    for all possible errors e, check matrix (or check function) H,
    and action matrix (or action function) A_{l}.
    '''

    # the literal string for representing the set of States
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='States', 
            latex_format=r'\mathcal{S}_{\ell}',
            styles=styles)

    def membership_object(self, element):
        from . import StatesMembership
        return StatesMembership(element, self)

    def nonmembership_object(self, element):
        from . import StatesNonmembership
        return StatesNonmembership(element, self)


class StatesMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    augmented syndrome states.

    UNDER CONSTRUCTION, with the code below borrowed from the
    logic/sets/Union class and serving as a placeholder.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    # def side_effects(self, judgment):
    #     '''
    #     TBA.
    #     '''
    #     yield self.unfold

    # @equality_prover('defined', 'define')
    # def definition(self, **defaults_config):
    #     '''
    #     Deduce and return 
    #         [element in (A union B ...)] = 
    #         [(element in A) or (element in B) ...]
    #     where self = (A union B ...).
    #     '''
    #     from . import union_def
    #     element = self.element
    #     operands = self.domain.operands
    #     _A = operands
    #     _m = _A.num_elements()
    #     return union_def.instantiate(
    #             {m: _m, x: element, A: _A}, auto_simplify=False)

    # def as_defined(self):
    #     '''
    #     From self=[elem in (A U B U ...)], return
    #     [(element in A) or (element in B) or ...].
    #     '''
    #     from proveit.logic import Or, InSet
    #     element = self.element
    #     return Or(*self.domain.operands.map_elements(
    #             lambda subset : InSet(element, subset)))

    # @prover
    # def unfold(self, **defaults_config):
    #     '''
    #     From [element in (A union B ...)], derive and return
    #     [(element in A) or (element in B) ...],
    #     where self represents [element in (A union B ...)].
    #     '''
    #     from . import membership_unfolding
    #     element = self.element
    #     operands = self.domain.operands
    #     _A = operands
    #     _m = _A.num_elements()
    #     return membership_unfolding.instantiate(
    #         {m: _m, x: element, A: _A}, auto_simplify=False)

    # @prover
    # def conclude(self, **defaults_config):
    #     '''
    #     Called on self = [elem in (A U B U ...)], and knowing or
    #     assuming [[elem in A] OR [elem in B] OR ...], derive and
    #     return self.
    #     '''
    #     from . import membership_folding
    #     element = self.element
    #     operands = self.domain.operands
    #     _A = operands
    #     _m = _A.num_elements()
    #     return membership_folding.instantiate({m: _m, x: element, A: _A})


class State(Function):
    '''
    State(syndrome, action, logical_obs) represents the augmented
    syndrome state tuple S_{l}(syndrome, action) specified by the
    detector 'syndrome' set and logical_obs-related 'action' (where
    the action is 0 or 1).
    
    This class is meant to allow the explicit specification of states
    such as (EmptySet, 0) or ({a, b, ..., m}, 1), instead of specifying
    the state in terms of the error set e. For the error-specified
    state, see the ErrorState class.
    '''

    # Literal operator for the State function,
    # but see further below for actual string and latex forms.
    _operator_ = Literal(
            string_format='state',
            latex_format=r'\textrm{state}',
            theory=__file__)

    def __init__(self, syndrome, action, logical_obs=None, *, styles=None):
        '''
        Create the explicit augmented syndrome state tuple
        (syndrome, action), with respect to the logical observable
        logical_obs (if any).
        '''
        
        # (1) Build the list of (keyword, expression) pairs
        items = [
            ("syndrome", syndrome),
            ("action", action)
        ]
        
        # (2) Add optional logical observable only if
        #     it was actually provided
        if logical_obs is not None:
            items.append(("logical_observable", logical_obs))
        
        # (3) Initialize NamedExprs with the list of tuples
        operands = NamedExprs(*items)
        
        # (4) Call Function's init
        super().__init__(self._operator_, operands=operands, styles=styles)

    def string(self, **kwargs):
        str_format = ('(' + self.syndrome.string()
                + ', ' + self.action.string() + ')')
        if hasattr(self, 'logical_observable'):
            str_format += '_{' + self.logical_observable.string() + '}'
        return str_format

    def latex(self, **kwargs):
        latex_str = (r'(' + self.syndrome.latex()
                + r', ' + self.action.latex() + r')')
        if hasattr(self, 'logical_observable'):
            latex_str += r'_{' + self.logical_observable.latex() + r'}'
        return latex_str


class ErrorState(Function):
    '''
    ErrorState(l, e) represents the augmented syndrome state

        (H e, A_{l} e)

    for error e and logical observable l.
    '''

    # Literal operator for the ErrorState function,
    # but see further below for actual string and latex forms.
    _operator_ = Literal(
            string_format='err_state',
            latex_format=r'\textrm{err\_state}',
            theory=__file__)

    def __init__(self, l, e, *, styles=None):
        '''
        Create State(l, e), as S_{l}(e), the augmented syndrome state
        (H e, A_{l} e).
        '''
        super().__init__(
                self._operator_, (l, e), styles=styles)

    def string(self, **kwargs):
        return ('S_{' + self.operands[0].string()
                + '}(' + self.operands[1].string() + ')')

    def latex(self, **kwargs):
        return (r'S_{' + self.operands[0].latex()
                + r'}(' + self.operands[1].latex() + r')')


class StateSyndrome(Function):
    '''
    StateSyndrome(S) represents the syndrome H(e) of the given augmented
    syndrome state S = (H(e), A_{l}(e)). This is useful when working
    with expressions utilizing an abstract state instead of the more
    concrete tuple (H(e), A_{l}(e)) when you end up also needing or
    wanting to refer to the state's syndrome component H(e).

    If the state S is an explicit State such as (D, i),
    StateSyndrome(S) represents the syndrome D. If the state S is
    an ErrorState of the form ErrorState(l, e), then StateSyndrome(S)
    represents the syndrome H(e).
    '''

    # operator for the StateSyndrome function.
    _operator_ = Literal(
            string_format='SYN',
            latex_format=r'\textsc{syn}',
            theory=__file__)

    def __init__(self, s, *, styles=None):
        '''
        Create StateSyndrome(s), as StateSyn(s), the syndrome
        associated with augmented syndrome state s
        '''
        super().__init__(
                StateSyndrome._operator_, s, styles=styles)


class StateAction(Function):
    '''
    StateAction(s) represents the logical l-relative "action" of the
    given augmented syndrome state s = (H(e), A_{l}(e)). This is useful
    when working with expressions utilizing an abstract state instead
    of the more concrete tuple (H(e), A_{l}(e)) when you end up also
    wanting to refer to the state's action component A_{l}(e).

    If the state S is an explicit State such as (D, i),
    StateAction(S) represents the logical action i. If the state S is
    an ErrorState of the form ErrorState(l, e), then StateAction(S)
    represents the logical action A_{l}(e).
    '''

    # operator for the StateAction function.
    _operator_ = Literal(
            string_format='ACT',
            latex_format=r'\textsc{act}',
            theory=__file__)

    def __init__(self, s, *, styles=None):
        '''
        Create StateAction(s), as ACT(s), the "action"
        associated with augmented syndrome state s.
        '''
        super().__init__(
                StateAction._operator_, s, styles=styles)


class AllStatesGraphLiteral(Literal):
    '''
    AllStatesGraphLiteral() (formatted as G_{states} in outputs)
    represents the graph G = (V, E) where the the set V of vertices
    is the sets of all possible augmented syndrome states S_{l}, and
    the set E of (directed) edges is the set of all ordered pairs
    (s, s'), where:

      * s, s' in S_{l};
      * [ACT(s)=0 AND ACT(s')=1] OR
        [ACT(s)=1 AND v(s) in (SYN(s) - SYN(s'))]

    where: ACT(s) is the logical action (0 or 1) for state s,
           SYN(s) is the syndrome for state s,
           and v(s) is the function that determines the next detector
                    to deactivate given state s.

    'AllStatesGraph' is then defined in the QEC2 common notebook as
    AllStatesGraph = AllStatesGraphLiteral().
    '''

    # the literal string for representing the AllStatesGraphLiteral
    def __init__(self, *, styles=None):
        Literal.__init__(
            self, string_format='G_{S_l}', 
            latex_format=r'G_{S_{\ell}}',
            styles=styles)


class CheckFunction(Function):
    '''
    CheckFunction(e) is a function version of the 'check matrix',
    taking an error e as input (and recall that an error e is just
    a set of faults) and producing/representing a syndrome output
    (i.e., a set of checks or detectors)
    '''

    # operator for the CheckFunction function.
    _operator_ = Literal(
            string_format='H',
            latex_format=r'H\!',
            theory=__file__)

    def __init__(self, e, *, styles=None):
        '''
        Create CheckFunction(e), as H(e), the syndrome associated
        with error e.
        '''
        super().__init__(
                CheckFunction._operator_, e, styles=styles)


class ActionFunction(Function):
    '''
    ActionFunction(l, e) is a function version of the 'action matrix',
    taking a logical operator l and error e as input (and recall that
    an error e is just a set of faults) and producing/representing 
    the logical action (relative to the logical operator l), which
    should be 0 (no action) or 1 (logical l applied).
    '''

    # operator for the ActionFunction function.
    _operator_ = Literal(
            string_format='A',
            latex_format=r'A',
            theory=__file__)

    def __init__(self, l, e, *, styles=None):
        '''
        Create ActionFunction(e), as A_{l}(e), the logical action
        l resulting from error e.
        '''
        super().__init__(
                ActionFunction._operator_, (l, e), styles=styles)

    def string(self, **kwargs):
        return ('A_{' + self.operands[0].string()
                + '}(' + self.operands[1].string() + ')')

    def latex(self, **kwargs):
        return (r'A_{' + self.operands[0].latex()
                + r'}(' + self.operands[1].latex() + r')')


class EdgeFaults(Function):
    '''
    EdgeFaults(s, s') represents the set of faults (possibly errors?)
    each of which can take augmented syndrome state s to augmented
    syndrome state s'.
    If s = (D, j) and s' = (D', j'), then we have:

      [f in EdgeFaults(s, s')] =
      [D ∆ (H({f})) = D']

    where H is our check matrix function.
    We use the class name 'EdgeFaults' because we envision the faults
    as taking state s to state s' in the AllStatesGraph, the vertices
    of which are the States and edge transitions from state to state
    represent a choice of syndrome component to eliminate.
    '''

    # The literal operator for the EdgeFaults function.
    _operator_ = Literal(
            string_format='EdgeFaults',
            latex_format=r'\textrm{EdgeFaults}',
            theory=__file__)

    def __init__(self, s, t, *, styles=None):
        '''
        Create/represent EdgeFaults(s, t), the set of faults each of
        which takes state s to state t.
        '''
        super().__init__(
                self._operator_, (s, t), styles=styles)

    def membership_object(self, element):
        from . import EdgeFaultsMembership
        return EdgeFaultsMembership(element, self)


class EdgeFaultsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    EdgeFaults(s, s'), the set of faults that each take state s
    to state s'.

    UNDER CONSTRUCTION. See the logic/sets/Union class for related
    example code.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)


class Realizations(Function):
    '''
    Realizations(p, G), for some path p = (p1, p2, ..., pn) in a graph
    G, where p1, p2, ..., pn are all augmented syndrome states, is the
    set of sequences of faults, each sequence (f1, f2, ..., fm)
    corresponding to the path p, in the sense that the sequence of
    faults "produces" the sequence of state vertices p2, ..., pn,
    beginning at p1, by having f_{i} take state p_{i} to state p_{i+1}.
    This is somewhat difficult to describe. An element of
    Realizations(p, G) is a sequence of faults that "produces" the
    the sequence p2, ..., pn of states beginning at state p1. There
    might be more than one such fault sequence that can produce the
    same sequence of states.
    '''

    # The literal operator for the Realizations function.
    _operator_ = Literal(
            string_format='Realizations',
            latex_format=r'\textrm{Realizations}',
            theory=__file__)

    def __init__(self, p, G, *, styles=None):
        '''
        Create/represent Realizations(p, G), the set of fault sequences
        each of which produce the vertex sequence p = (p1,...,pn) in
        graph G.
        '''
        self.graph = G
        self.path = p
        super().__init__(
                self._operator_, (p, G), styles=styles)

    def membership_object(self, element):
        from . import RealizationsMembership
        return RealizationsMembership(element, self)


class RealizationsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    Realizations(p, G), the set of fault sequences corresponding
    to the path p in graph G.

    UNDER CONSTRUCTION. See the logic/sets/Union class for related
    example code.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    # def side_effects(self, judgment):
    #     '''
    #     Unfold the enumerated set membership as a side-effect.
    #     '''
    #     yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Deduce and return 

          [(f1, f2, ..., f_{n-1}) in Realizations(s1, s2, ..., sn)] = 
          Forall_{i in {1..n-1}}[f_i in EdgeFaults(s_{i}, s_{i+1})]

        Obviously this only works if the element is a fault sequence
        and the Realizations operand is an explicit sequence of graph
        nodes (or equal to such a sequence).
        '''
        from . import realizations_membership_def
        element = self.element               # a fault sequence
        _s_sub  = self.domain.operands[0]    # a node sequence (path)
        _n_sub  = _s_sub.num_elements()      # num elems in node seq
        _G_sub  = self.domain.operands[1]    # the graph context
        return realizations_membership_def.instantiate(
                {G:_G_sub, n:_n_sub, s:_s_sub, f:element})
