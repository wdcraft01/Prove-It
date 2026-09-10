from proveit import (
        b, e, f, i, n, s, A, B, D, G, equality_prover,
        Function, Literal, NamedExprs, Operation, prover,
        relation_prover, TransRelUpdater)
from proveit.logic import (
        And, Equals, InSet, SetMembership,
        SetNonmembership)
from proveit.logic.sets import Disjoint, Set
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

    def membership_object(self, element):
        from . import IrreducibleBufiloSetsMembership
        return IrreducibleBufiloSetsMembership(element, self)

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


class IrreducibleBufiloSetsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    irreducible BUFILOs, iBUFS.

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
        From [b in iBUFS], deduce and return the equality

            [b in iBUFS] = 
            [b in BUFS AND NotExists(b' in BUFS [b' subset b])]

        where the BufiloSets BUFS class is defined above.
        '''

        from . import irreducible_bufs_membership_def
        _b_sub = self.element
        return irreducible_bufs_membership_def.instantiate(
                {b: _b_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From [b in iBUFS], return the expression (NOT a Judgment):

            [b in BUFS AND NotExists(b' in BUFS [b' subset b])]

        where the BufiloSets BUFS class is defined above.
        '''
        from proveit.logic import And, NotExists
        from proveit.logic.sets import SubsetProper
        # from proveit.numbers import one
        from . import b_prime, BufiloSets
        element = self.element
        return And(InSet(element, BufiloSets),
                   NotExists(b_prime, SubsetProper(b_prime, element),
                             domain=BufiloSets))

    @prover
    def unfold(self, **defaults_config):
        '''
        From [b in iBUFS], deduce and return the Judgment:

            [b in BUFS AND NotExists(b' in BUFS [b' subset b])]

        where the BufiloSets BUFS class is defined above.
        '''
        from . import irreducible_bufs_membership_unfolding
        _b_sub = self.element
        return irreducible_bufs_membership_unfolding.instantiate(
            {b: _b_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        From self = [b in iBUFS], and knowing or assuming that 

            [b in BUFS AND NotExists(b' in BUFS [b' subset b])]

        where the BufiloSets BUFS class is defined above, derive and
        return self (as a Judgment).
        '''
        from . import irreducible_bufs_membership_folding
        _b_sub = self.element
        return irreducible_bufs_membership_folding.instantiate({b: _b_sub})


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

    def membership_object(self, element):
        from . import FaultsMembership
        return FaultsMembership(element, self)


class FaultsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set Faults of all
    faults.

    UNDER CONSTRUCTION.
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
        From self = [f in FAULTS], deduce and return ... what?
        '''
        raise NotImplementedError(
            "Sorry! FaultsMembership.definition() not yet implemented.")

    def as_defined(self):
        '''
        From self = [f in FAULTS], deduce and return ... what?
        '''
        raise NotImplementedError(
            "Sorry! FaultsMembership.definition() not yet implemented.")

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [f in FAULTS], deduce and return ... what?
        '''
        raise NotImplementedError(
            "Sorry! FaultsMembership.definition() not yet implemented.")

    @prover
    def conclude(self, **defaults_config):
        '''
        From self = [f in FAULTS], and knowing or assuming that 

            [f in e, for some error e in ERRS]

        derive and return self.
        '''
        raise NotImplementedError(
            "Sorry! FaultsMembership.definition() not yet implemented.")


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

    def membership_object(self, element):
        from . import ErrorsMembership
        return ErrorsMembership(element, self)


class ErrorsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    errors, Errors. An error e is simply a set of faults.

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
        From self = [e in ERRS], deduce and return the equality

            [e in ERRS] = 
            [Exists_{n in Natural} Exists_{f1, ..., fn in FAULTS}
                (e = {f1, ..., fn})]

        where FAULTS is the set of all faults.
        '''

        from . import errors_membership_def
        _e_sub = self.element
        return errors_membership_def.instantiate(
                {e: _e_sub}, auto_simplify=False)

    def as_defined(self):
        '''
        From self = [e in ERRS], return the expression (NOT a Judgment):

            [Exists_{n in Natural} Exists_{f1, ..., fn in FAULTS}
                (e = {f1, ..., fn})]

        where FAULTS is the set of all faults.
        '''
        from proveit.logic import Exists
        from . import f_one_to_n, Faults
        element = self.element
        return Exists(n, Exists((f_one_to_n),
               Equals(element, Set(f_one_to_n)),
               domain=Faults), domain=Natural)

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [e in ERRS], deduce and return the Judgment:

            [Exists_{n in Natural} Exists_{f1, ..., fn in FAULTS}
                (e = {f1, ..., fn})]

        where FAULTS is the set of all faults.
        '''
        from . import errors_membership_unfolding
        _e_sub = self.element
        return errors_membership_unfolding.instantiate(
            {e: _e_sub}, auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        From self = [e in ERRS], and knowing or assuming that 

            [Exists_{n in Natural} Exists_{f1, ..., fn in FAULTS}
                (e = {f1, ..., fn})]

        where FAULTS is the set of all faults, derive and return
        self.
        '''
        from . import errors_membership_folding
        _e_sub = self.element
        return errors_membership_folding.instantiate({e: _e_sub})


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

    def membership_object(self, element):
        from . import SyndromesMembership
        return SyndromesMembership(element, self)


class SyndromesMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    Syndromes, where a Syndrome is a subset of the set of Detectors.

    UNDER CONSTRUCTION
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
        From self = [s in Syndromes], deduce and return
        
            [s in Syndromes] = [s ⊆ Detectors]
        '''
        element = self.element

        from . import syndromes_membership_def
        return syndromes_membership_def.instantiate(
                {s:element})

    def as_defined(self):
        '''
        From self = [s in Syndromes], construct and return the
        expression (NOT a Judgment):
        
            [s ⊆ Detectors]
        '''
        element = self.element

        from . import Detectors
        from proveit.logic.sets import SubsetEq

        return SubsetEq(element, Detectors)

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [s in Syndromes], deduce and return
        
            |- [s ⊆ Detectors]
        '''
        element = self.element

        from . import syndromes_membership_unfolding
        return syndromes_membership_unfolding.instantiate(
                {s:element})

    @prover
    def conclude(self, **defaults_config):
        '''
        From self = [s in Syndromes], and knowing or assuming that:
        
            [s ⊆ Detectors]

        deduce and return self.
        '''
        element = self.element

        from . import syndromes_membership_folding
        return syndromes_membership_folding.instantiate(
                {s:element})


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


class StatesMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set of all
    States, which is the set of all augmented syndrome states.

    UNDER CONSTRUCTION
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
        From self = [s in States], deduce and return
        
            [s in States] = 
            [SYN(s) ⊆ Detectors AND ACT(s) in {0,1}]
        
        and from self = [State(D, i) in States], deduce and return

            [State(D, i) in States] = 
            [D ⊆ Detectors AND i in {0,1}]
        '''
        element = self.element

        if not isinstance(element, State):
            from . import states_membership_def
            return states_membership_def.instantiate(
                    {s:element})

        from . import states_membership_tuple_def
        _D_sub = element.syndrome
        _i_sub = element.action
        return states_membership_tuple_def.instantiate(
                {D:_D_sub, i:_i_sub})

    def as_defined(self):
        '''
        From self = [s in States], construct and return the expression
        (NOT a Judgment):
        
            [SYN(s) ⊆ Detectors AND ACT(s) in {0,1}]
        
        and from self = [State(D, i) in States], construct and return
        the expression (NOT a Judgment):

            [D ⊆ Detectors AND i in {0,1}]
        '''
        element = self.element

        from . import Detectors, StateAction, StateSyndrome
        from proveit.logic.sets import SubsetEq
        from proveit.numbers import zero, one

        if not isinstance(element, State):
            # The state is generic
            return And(SubsetEq(StateSyndrome(element), Detectors),
                       InSet(StateAction(element), Set(zero, one)))

        # The state is of the form State(D, i)
        _D = element.syndrome
        _i = element.action
        return And(SubsetEq(_D, Detectors), InSet(_i, Set(zero, one)))

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [s in States], and knowing or assuming self
        to be True, deduce and return
        
            [SYN(s) ⊆ Detectors AND ACT(s) in {0,1}],
        
        and from self = [State(D, i) in States], and knowing or
        assuming self to be True, deduce and return

            [D ⊆ Detectors AND i in {0,1}]
        '''
        element = self.element

        if not isinstance(element, State):
            from . import states_membership_unfolding
            return states_membership_unfolding.instantiate(
                    {s:element})

        from . import states_membership_tuple_unfolding
        _D_sub = element.syndrome
        _i_sub = element.action
        return states_membership_tuple_unfolding.instantiate(
                {D:_D_sub, i:_i_sub})

    @prover
    def conclude(self, **defaults_config):
        '''
        From self = [s in States], and knowing or assuming:

            [SYN(s) ⊆ Detectors AND ACT(s) in {0,1}]

        to be True, deduce and return self.
        
        And from self = [State(D, i) in States], and knowing or
        assuming

            [D ⊆ Detectors AND i in {0,1}]

        to be True, deduce and return self.

        '''
        element = self.element

        if not isinstance(element, State):
            from . import states_membership_folding
            return states_membership_folding.instantiate(
                    {s:element})

        from . import states_membership_tuple_folding
        _D_sub = element.syndrome
        _i_sub = element.action
        return states_membership_tuple_folding.instantiate(
                {D:_D_sub, i:_i_sub})


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
      [D' = D ∆ (H({f}))  AND j' = j ⊕ A_{l}({f})]

    where:

      H is our check matrix function, CheckFunction;
      A is our action matrix function, ActionFunction;
      ∆ denotes the set-theoretic symmetric difference;
      ⊕ denotes mod-2 addition

    We use the class name 'EdgeFaults' because we envision the faults
    as taking state s to state s' in the AllStatesGraph, the vertices
    of which are the States and edge transitions from state to state
    represent a choice of syndrome component(s) to eliminate.
    '''

    # The literal operator for the EdgeFaults function.
    _operator_ = Literal(
            string_format='EdgeFaults',
            latex_format=r'\textrm{EdgeFaults}',
            theory=__file__)

    def __init__(self, *operands, styles=None):
        '''
        Create/represent EdgeFaults(e) or EdgeFaults(s, t), the set
        of faults each of which takes state s to state t (via edge e,
        which then implicitly determines state s and state t).
        '''
        if len(operands) == 2:
            # the operands consist of an edge e and a graph G
            self.edge = operands[0]
            self.graph = operands[1]
        elif len(operands) == 3:
            # the operands consist of two nodes s, t (defining an edge),
            # followed by a graph G
            from proveit import ExprTuple
            self.edge = ExprTuple(operands[0], operands[1])
            self.graph = operands[2]
        else:
            # wrong number of operands supplied
            raise ValueError(
                f"Usage: EdgeFaults(e, G) or EdgeFaults(s, t, G), "
                f"using two or three operands, where the operands consist "
                f"of either: (1) a single edge 'e' and a graph 'G' "
                f"containing the supplied edge, OR (2) two adjacent nodes "
                f"'s' and 't' and the graph 'G' containing those nodes. "
                f"Instead, the supplied operands were: {operands}.")

        super().__init__(
                self._operator_, (self.edge, self.graph), styles=styles)

    def string(self, **kwargs):
        return ('F_{edge, ' + self.graph.string()
                + '}(' + self.edge.string() + ')')

    def latex(self, **kwargs):
        from proveit import ExprTuple
        if not isinstance(self.edge, ExprTuple):
            return (r'\mathcal{F}_{' + self.graph.latex()
                    + r'}^{\text{edge}}(' + self.edge.latex() + r')')
        return (r'\mathcal{F}_{' + self.graph.latex()
                    + r'}^{\text{edge}}('
                    + self.edge[0].latex() + ', '
                    + self.edge[1].latex() + r')')

    def membership_object(self, element):
        from . import EdgeFaultsMembership
        return EdgeFaultsMembership(element, self)


class EdgeFaultsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    EdgeFaults(e, G) or EdgeFaults(s, s', G), the set of faults
    that each take state s to state s' (or along edge e).

    UNDER CONSTRUCTION. See the logic/sets/Union class for related
    example code.
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
        From self = [f in EdgeFaults(s, s', G)], deduce and return the
        equality

          [f in EdgeFaults(s, s', G)] =
          [D' = D ∆ (H({f}))  AND j' = j ⊕ A_{l}({f})]

        where:

          s, s' = (D, j), (D', j')
          H is our check matrix function, CheckFunction;
          A is our action matrix function, ActionFunction;
          ∆ denotes the set-theoretic symmetric difference;
          ⊕ denotes mod-2 addition.

        If the edge (s, s') is specified abstractly simply as 'e',
        with no specified end-nodes, then the definition() method
        fails.
        '''
        from proveit import ExprTuple
        if not isinstance(self.domain.edge, ExprTuple):
            raise NotImplementedError(
                f"EdgeFaultsMembership.definition() method implemented "
                f"only for cases where the edge has explicit "
                f"end-nodes specified, which is not the case for "
                f"the supplied edge: {self.domain.edge}. ")
        from . import edge_faults_membership_def, s_prime
        _f_sub = self.element
        _s_sub = self.domain.edge[0]
        _s_prime_sub = self.domain.edge[1]
        
        return edge_faults_membership_def.instantiate(
                {f:_f_sub, s:_s_sub, s_prime:_s_prime_sub},
                auto_simplify=False)

    def as_defined(self):
        '''
        From self = [f in EdgeFaults(s, s')], return the expression
        (NOT a judgment):

          [D' = D ∆ (H({f}))  AND j' = j ⊕ A_{l}({f})]

        where:

          s, s' = (D, j), (D', j')
          H is our check matrix function, CheckFunction;
          A is our action matrix function, ActionFunction;
          ∆ denotes the set-theoretic symmetric difference;
          ⊕ denotes mod-2 addition.

        If the edge (s, s') is specified abstractly simply as 'e',
        with no specified end-nodes, then the as_defined() method
        fails.
        '''
        from proveit import ExprTuple
        from proveit.logic import And, Equals
        from proveit.logic.sets import Set, SymmetricDifference
        from proveit.numbers import two, Add, Mod
        from . import (
            _ell, ActionFunction, f_one_to_n, Faults, StateAction, StateSyndrome)

        if not isinstance(self.domain.edge, ExprTuple):
            raise NotImplementedError(
                f"EdgeFaultsMembership.as_defined() method implemented "
                f"only for cases where the edge has explicit "
                f"end-nodes specified, which is not the case for "
                f"the supplied edge: {self.domain.edge}. ")

        element = self.element
        _s = self.domain.edge[0]
        _s_prime = self.domain.edge[1]

        return And(
            Equals(StateSyndrome(_s_prime),
                   SymmetricDifference(StateSyndrome(_s),
                                       StateSyndrome(Set(element)))),
            Equals(StateAction(_s_prime),
                   Mod(Add(StateAction(_s),
                           ActionFunction(_ell, Set(element))), two)))

    @prover
    def unfold(self, **defaults_config):
        '''
        From self = [f in EdgeFaults(s, s')], deduce and return the
        Judgment

          [D' = D ∆ (H({f}))  AND j' = j ⊕ A_{l}({f})]

        where:

          s, s' = (D, j), (D', j')
          H is our check matrix function, CheckFunction;
          A is our action matrix function, ActionFunction;
          ∆ denotes the set-theoretic symmetric difference;
          ⊕ denotes mod-2 addition.

        If the edge (s, s') is specified abstractly simply as 'e',
        with no specified end-nodes, then the unfold() method
        fails.
        '''
        from proveit import ExprTuple
        from . import edge_faults_membership_unfolding, s_prime

        if not isinstance(self.domain.edge, ExprTuple):
            raise NotImplementedError(
                f"EdgeFaultsMembership.as_defined() method implemented "
                f"only for cases where the edge has explicit "
                f"end-nodes specified, which is not the case for "
                f"the supplied edge: {self.domain.edge}. ")

        _f_sub       = self.element
        _s_sub       = self.domain.edge[0]
        _s_prime_sub = self.domain.edge[1]
        _G_sub       = self.domain.graph

        return edge_faults_membership_unfolding.instantiate(
            {G:_G_sub, f:_f_sub, s:_s_sub, s_prime:_s_prime_sub},
            auto_simplify=False)

    @prover
    def conclude(self, **defaults_config):
        '''
        From self = [f in EdgeFaults(s, s')], and knowing or assuming
        that 

            [D' = D ∆ (H({f}))  AND j' = j ⊕ A_{l}({f})]

        where:

          s, s' = (D, j), (D', j')
          H is our check matrix function, CheckFunction;
          A is our action matrix function, ActionFunction;
          ∆ denotes the set-theoretic symmetric difference;
          ⊕ denotes mod-2 addition,

        derive and return self.

        If the edge (s, s') is specified abstractly simply as 'e',
        with no specified end-nodes, then the conclude() method
        fails.

        '''
        from proveit import ExprTuple
        from . import edge_faults_membership_folding, s_prime

        if not isinstance(self.domain.edge, ExprTuple):
            raise NotImplementedError(
                f"EdgeFaultsMembership.as_defined() method implemented "
                f"only for cases where the edge has explicit "
                f"end-nodes specified, which is not the case for "
                f"the supplied edge: {self.domain.edge}. ")

        _f_sub       = self.element
        _s_sub       = self.domain.edge[0]
        _s_prime_sub = self.domain.edge[1]
        _G_sub       = self.domain.graph
        return edge_faults_membership_folding.instantiate(
            {G:_G_sub, f: _f_sub, s:_s_sub, s_prime:_s_prime_sub})


class Realizations(Function):
    '''
    Realizations(E, G), for some sequence E = (e1, e2, ..., en) of
    edges e1, e2, ..., en in graph G, where the edges are
    conceptualized as edges between augmented syndrome states, is the
    set of fault sequences of the form (f1, f2, ..., fn), each of
    which corresponds to the sequence (e1, e2, ..., en) of edges,
    in the sense that fault f_{i} takes state s_{i} to state s_{j}
    along edge e_{i}.
    This is somewhat difficult to describe. An element of
    Realizations(E, G) is a sequence of faults that correspond to
    "traveling" along the sequence of edges (although the edges here
    are not required to form an actual path in graph G). As implied,
    there might be more than one such fault sequence that corresponds
    to the same sequence of edges in G.
    '''

    # The literal operator for the Realizations function.
    _operator_ = Literal(
            string_format='Realizations',
            latex_format=r'\textrm{Realizations}',
            theory=__file__)

    def __init__(self, E, G, *, styles=None):
        '''
        Create/represent Realizations(p, G), the set of fault
        sequences each sequence corresponding to the edge sequence
        E = (e1,...,en) in graph G.
        '''
        self.graph = G
        self.edges = E
        super().__init__(
                self._operator_, (E, G), styles=styles)

    def membership_object(self, element):
        from . import RealizationsMembership
        return RealizationsMembership(element, self)


class RealizationsMembership(SetMembership):
    '''
    Defines methods that apply to membership in the set
    Realizations(E, G), the set of fault sequences corresponding
    to the edge sequence E = (e1, e1, ..., en) in graph G.
    '''

    def __init__(self, element, domain):
        SetMembership.__init__(self, element, domain)

    # def side_effects(self, judgment):
    #     '''
    #     Unfold the set membership as a side-effect?
    #     '''
    #     yield self.unfold

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Deduce and return the equality: 

        [(f1, f2, ..., f_n) in Realizations((e1, e2, ..., en), G] = 
        f1 in EdgeFaults(e1, G) AND ... AND f_n in EdgeFaults(e_n, G),

        the RHS being equivalent to:

            Forall_{i in {1..n}}[f_i in EdgeFaults(e_i, G)]

        This only works if the element is a fault sequence
        and the Realizations operand is an explicit sequence of graph
        edges, with the number of faults equal to the number of edges.
        Otherwise the definition method fails.
        '''

        from . import realizations_membership_def
        element = self.element               # a fault sequence, f
        _e_sub  = self.domain.operands[0]    # an edge sequence
        _n_sub  = element.num_elements()     # num elems in node seq
        _G_sub  = self.domain.operands[1]    # the graph context
        return realizations_membership_def.instantiate(
                {G:_G_sub, n:_n_sub, e:_e_sub, f:element})

    def as_defined(self):
        '''
        From self as:

          [(f1, f2, ..., f_n) in Realizations((e1, e2, ..., en), G],

        return the expression (NOT a judgment):

          f1 in EdgeFaults(e1, G) AND ... AND f_n in EdgeFaults(e_n, G),

        with that being equivalent to:

            Forall_{i in {1..n}}[f_i in EdgeFaults(e_i, G)]

        This only works if the element is a fault sequence and the
        Realizations operand is an explicit sequence of graph
        edges, with the number of faults equal to the number of edges.
        Otherwise the as_defined() method fails.
        '''
        raise NotImplementedError(
            f"Sorry, RealizationsMembership.as_defined() is not yet "
            f"implemented.")

    @prover
    def unfold(self, **defaults_config):
        '''
        From self:

          [(f1, f2, ..., f_n) in Realizations((e1, e2, ..., en), G]

        deduce and return the Judgment:

          f1 in EdgeFaults(e1, G) AND ... AND f_n in EdgeFaults(e_n, G),

        with that being equivalent to:

            Forall_{i in {1..n}}[f_i in EdgeFaults(e_i, G)]

        This only works if the element is a fault sequence
        and the Realizations operand is an explicit sequence of graph
        edges, with the number of faults equal to the number of edges.
        Otherwise the definition method fails.
        '''

        from . import realizations_membership_unfolding
        element = self.element               # a fault sequence, f
        _e_sub  = self.domain.operands[0]    # an edge sequence
        _n_sub  = element.num_elements()     # num elems in fault seq
        _G_sub  = self.domain.operands[1]    # the graph context
        return realizations_membership_unfolding.instantiate(
                {G:_G_sub, n:_n_sub, e:_e_sub, f:element})

    @prover
    def conclude(self, **defaults_config):
        '''
        From self

          [(f1, f2, ..., f_n) in Realizations((e1, e2, ..., en), G],

        and knowing or assuming that

          f1 in EdgeFaults(e1, G) AND ... AND f_n in EdgeFaults(e_n, G),

        with that being equivalent to:

          Forall_{i in {1..n}}[f_i in EdgeFaults(e_i, G)],

        deduce and return self.

        This only works if the element is a fault sequence
        and the Realizations operand is an explicit sequence of graph
        edges, with the number of faults equal to the number of edges.
        Otherwise the definition method fails.
        '''

        from . import realizations_membership_folding
        element = self.element               # a fault sequence, f
        _e_sub  = self.domain.operands[0]    # an edge sequence
        _n_sub  = element.num_elements()     # num elems in fault seq
        _G_sub  = self.domain.operands[1]    # the graph context
        return realizations_membership_folding.instantiate(
                {G:_G_sub, n:_n_sub, e:_e_sub, f:element})
        
