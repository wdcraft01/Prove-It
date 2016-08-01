from proveit import BinaryOperation, USE_DEFAULTS, ProofFailure, asExpression
from proveit import Variable, MultiVariable, Literal, Operation, ExpressionList, Etcetera, ExpressionTensor, Block, safeDummyVar
from proveit.common import A, P, X, f, x, y, z
from transitivity_search import transitivitySearch

pkg = __package__

EQUALS = Literal(pkg, '=')

class Equals(BinaryOperation):
    # map Expressions to sets of KnownTruths of equalities that involve the Expression
    # on the left hand or right hand side.
    knownEqualities = dict()
    
    def __init__(self, a, b):
        BinaryOperation.__init__(self, EQUALS, a, b)
        self.lhs = a
        self.rhs = b
        
    def deduceSideEffects(self, knownTruth):
        '''
        Record the knownTruth in Equals.knownEqualities, associated from
        the left hand side and the right hand side.  This information may
        be useful for concluding new equations via transitivity.  Also
        derive the reversed form, as a side effect.  If the right side
        is TRUE or FALSE, `deriveViaBooleanEquality` as a side effect.
        '''
        from proveit.logic import TRUE, FALSE
        Equals.knownEqualities.setdefault(self.lhs, set()).add(knownTruth)
        Equals.knownEqualities.setdefault(self.rhs, set()).add(knownTruth)
        if (self.lhs != self.rhs):
            # automatically derive the reversed form which is equivalent
            self.deriveReversed(knownTruth.assumptions)
        if self.rhs in (TRUE, FALSE):
            # automatically derive A from A=TRUE or Not(A) from A=FALSE
            self.deriveViaBooleanEquality(knownTruth.assumptions)
        
    def conclude(self, assumptions):
        '''
        Use other equalitieis that are known to be true to try to conclude 
        this equality via transitivity.  For example, if a=b, b=c, and c=d are 
        known truths (under the given assumptions), we can conclude that a=d
        (under these assumptions).
        '''
        from proveit.logic import TRUE, FALSE
        if self.lhs==self.rhs:
            self.concludeViaReflexivity()
        if self.lhs or self.rhs in (TRUE, FALSE):
            try:
                self.concludeBooleanEquality(assumptions)
            except ProofFailure:
                pass
        # Use a breadth-first search approach to find the shortest
        # path to get from one end-point to the other.
        return transitivitySearch(self, assumptions)
                
    @staticmethod
    def knownRelationsFromLeft(expr, assumptionsSet):
        '''
        For each KnownTruth that is an Equals involving the given expression on
        the left hand side, yield the KnownTruth and the right hand side.
        '''
        for knownTruth in Equals.knownEqualities.get(expr, frozenset()):
            if knownTruth.lhs == expr:
                if assumptionsSet.issuperset(knownTruth.assumptions):
                    yield (knownTruth, knownTruth.rhs)
    
    @staticmethod
    def knownRelationsFromRight(expr, assumptionsSet):
        '''
        For each KnownTruth that is an Equals involving the given expression on
        the right hand side, yield the KnownTruth and the left hand side.
        '''
        for knownTruth in Equals.knownEqualities.get(expr, frozenset()):
            if knownTruth.rhs == expr:
                if assumptionsSet.issuperset(knownTruth.assumptions):
                    yield (knownTruth, knownTruth.lhs)
            
    @classmethod
    def operatorOfOperation(subClass):
        return EQUALS    

    def concludeViaReflexivity(self):
        '''
        Prove and return self of the form x = x.
        '''
        from axioms import equalsReflexivity
        assert self.lhs == self.rhs
        return equalsReflexivity.specialize({x:self.lhs})
            
    def deriveReversed(self, assumptions=USE_DEFAULTS):
        '''
        From x = y derive y = x.  This derivation is an automatic side-effect.
        '''
        from axioms import equalsSymmetry
        return equalsSymmetry.specialize({x:self.lhs, y:self.rhs}).deriveConclusion(assumptions)

    def transitivityImpl(self, otherEquality, assumptions=USE_DEFAULTS):
        '''
        From x = y (self) and the given y = z (otherEquality) derive and return 
        (y=z) => (x = z) assuming self.
        Also works more generally as long as there is a common side to the equations.
        '''
        from axioms import equalsTransitivity
        otherEquality = asExpression(otherEquality)
        assert isinstance(otherEquality, Equals)
        if self.rhs == otherEquality.lhs:
            # from x = y, y = z, derive y = z => x = z assuing x = y
            result = equalsTransitivity.specialize({x:self.lhs, y:self.rhs, z:otherEquality.rhs}).deriveConclusion(assumptions)
            return result
        elif self.lhs == otherEquality.lhs:
            # from y = x and y = z, derive y = z => x = z assuing x = y
            return self.deriveReversed(assumptions).transitivityImpl(otherEquality, assumptions)
        elif self.lhs == otherEquality.rhs:
            # from y = x and z = y, derive y = z => x = z assuing x = y
            return self.deriveReversed(assumptions).transitivityImpl(otherEquality.deriveReversed(assumptions), assumptions)
        elif self.rhs == otherEquality.rhs:
            # from x = y and z = y, derive y = z => x = z assuing x = y
            return self.transitivityImpl(otherEquality.deriveReversed(assumptions), assumptions)
        else:
            assert False, 'transitivity cannot be applied unless there is something in common in the equalities'
            
    def applyTransitivity(self, otherEquality, assumptions=USE_DEFAULTS):
        '''
        From x = y (self) and y = z (otherEquality) derive and return x = z.
        Also works more generally as long as there is a common side to the equations.
        '''
        return self.transitivityImpl(otherEquality, assumptions).deriveConclusion(assumptions)
        
    def deriveViaBooleanEquality(self, assumptions=USE_DEFAULTS):
        '''
        From A = TRUE derive A, or from A = FALSE derive Not(A).  This derivation
        is an automatic side-effect.
        Note, see deriveStmtEqTrue or Not.equateNegatedToFalse for the reverse process.
        '''
        from proveit.logic import TRUE, FALSE        
        from proveit.logic.boolean.axioms import eqTrueElim
        from proveit.logic.boolean.negation.theorems import notFromEqFalse
        if self.rhs == TRUE:
            return eqTrueElim.specialize({A:self.lhs}).deriveConclusion(assumptions) # A
        elif self.rhs == FALSE:
            return notFromEqFalse.specialize({A:self.lhs}).deriveConclusion(assumptions) # Not(A)
        
    def deriveContradiction(self):
        '''
        From A=FALSE, derive A=>FALSE.
        '''
        from proveit.logic import FALSE        
        from theorems import contradictionFromFalseEquivalence, contradictionFromFalseEquivalenceReversed
        if self.rhs == FALSE:
            return contradictionFromFalseEquivalence.specialize({A:self.lhs}).deriveConclusion()
        elif self.lhs == FALSE:
            return contradictionFromFalseEquivalenceReversed.specialize({A:self.rhs}).deriveConclusion()
    
    def concludeBooleanEquality(self, assumptions=USE_DEFAULTS):
        '''
        Prove and return self of the form (A=TRUE) assuming A, (TRUE=A) assuming A, 
        A=FALSE assuming Not(A), FALSE=A assuming Not(A), [Not(A)=FALSE] assuming A, or [FALSE=Not(A)] assuming A.
        '''
        from proveit.logic import TRUE, FALSE, Not        
        from proveit.logic.boolean.axioms import eqTrueIntro
        from proveit.logic.boolean.theorems import eqTrueRevIntro
        from proveit.logic.boolean.negation.theorems import eqFalseFromNegation, eqFalseRevFromNegation
        if self.rhs == TRUE:
            return eqTrueIntro.specialize({A:self.lhs}).deriveConclusion(assumptions)
        elif self.rhs == FALSE:
            if isinstance(self.lhs, Not):
                return eqFalseFromNegation.specialize({A:self.lhs.operands}).deriveConclusion(assumptions)
            else:
                return Not(self.lhs).equateNegatedToFalse(assumptions)
        elif self.lhs == TRUE:
            return eqTrueRevIntro.specialize({A:self.rhs}).deriveConclusion(assumptions)
        elif self.lhs == FALSE:
            if isinstance(self.rhs, Not):
                return eqFalseRevFromNegation.specialize({A:self.rhs.operands}).deriveConclusion(assumptions)
            else:
                return Not(self.rhs).equateFalseToNegated(assumptions)
    
    def deriveIsInSingleton(self):
        '''
        From (x = y), derive (x in {y}).
        '''
        from proveit.logic.set_theory.axioms import singletonDef
        singletonDef.specialize({x:self.lhs, y:self.rhs}).deriveLeft()
    
    def _subFn(self, fnExpr, fnArg, subbing, replacement):
        if fnArg is None:
            dummyVar = safeDummyVar(self, fnExpr)
            if isinstance(replacement, ExpressionList):
                fnArg = Etcetera(MultiVariable(dummyVar))
            elif isinstance(replacement, ExpressionTensor):
                fnArg = Block(dummyVar)
            else:
                fnArg = dummyVar
            fnExpr = fnExpr.substituted({subbing:fnArg})
            if dummyVar not in fnExpr.freeVars():
                raise Exception('Expression to be substituted is not found within the expression that the substitution is applied to.')
        return fnExpr, fnArg
    
    def substitution(self, fnExpr, fnArg=None, assumptions=USE_DEFAULTS):
        '''
        From x = y, and given f(x), derive f(x)=f(y).  If fnArg is
        supplied, then the f function is defined as the lambda function
        f: fnArg -> fnExpr.  Otherwise, all occurences of self.lhs will be
        replaced with self.rhs inside fnExpr for this substitution.
        '''
        from axioms import substitution
        fnExpr, fnArg = self._subFn(fnExpr, fnArg, self.lhs, self.rhs)
        assert isinstance(fnArg, Variable) or isinstance(fnArg, Etcetera) or isinstance(fnArg, Block)
        return substitution.specialize({x:self.lhs, y:self.rhs, Operation(f, fnArg):fnExpr}).deriveConclusion(assumptions)
        
    def lhsStatementSubstitution(self, fnExpr, fnArg=None):
        '''
        From x = y, and given P(y), derive P(y)=>P(x).  
        If fnArg is supplied, then the P function is defined as the lambda function
        P: fnArg -> fnExpr.  Otherwise, all occurences of self.rhs will be
        replaced with self.lhs inside fnExpr for this substitution.        
        '''
        from theorems import lhsSubstitution
        fnExpr, fnArg = self._subFn(fnExpr, fnArg, self.rhs, self.lhs)
        assert isinstance(fnArg, Variable)
        return lhsSubstitution.specialize({x:self.lhs, y:self.rhs, Operation(P, fnArg):fnExpr}).deriveConclusion()
    
    def rhsStatementSubstitution(self, fnExpr, fnArg=None, assumptions=USE_DEFAULTS):
        '''
        From x = y, and given P(x), derive P(x)=>P(y).  
        If fnArg is supplied, then the P function is defined as the lambda function
        P: fnArg -> fnExpr.  Otherwise, all occurences of self.lhs will be
        replaced with self.rhs inside fnExpr for this substitution.   
        '''
        from theorems import rhsSubstitution
        fnExpr, fnArg = self._subFn(fnExpr, fnArg, self.lhs, self.rhs)        
        assert isinstance(fnArg, Variable)
        return rhsSubstitution.specialize({x:self.lhs, y:self.rhs, Operation(P, fnArg):fnExpr}).deriveConclusion(assumptions=assumptions)

    def lhsSubstitute(self, fnExpr, fnArg=None):
        '''
        From x = y, and given P(y), derive P(x) assuming P(y).  
        If fnArg is supplied, then the P function is defined as the lambda function
        P: fnArg -> fnExpr.  Otherwise, all occurences of self.rhs will be
        replaced with self.lhs inside fnExpr for this substitution.   
        '''
        substitution = self.lhsStatementSubstitution(fnExpr, fnArg)
        return substitution.deriveConclusion()
        
    def rhsSubstitute(self, fnExpr, fnArg=None, assumptions=USE_DEFAULTS):
        '''
        From x = y, and given P(x), derive P(y) assuming P(x).  
        If fnArg is supplied, then the P function is defined as the lambda function
        P: fnArg -> fnExpr.  Otherwise, all occurences of self.lhs will be
        replaced with self.rhs inside fnExpr for this substitution.   
        '''
        substitution = self.rhsStatementSubstitution(fnExpr, fnArg, assumptions)
        return substitution.deriveConclusion()

    def leftImplViaEquivalence(self):
        '''
        From A = B, derive B=>A
        '''
        return self.lhsStatementSubstitution(X, X)

    def rightImplViaEquivalence(self):
        '''
        From A = B, derive A=>B
        '''
        return self.rhsStatementSubstitution(X, X)
        
    def deriveRightViaEquivalence(self):
        '''
        From A = B, derive B (the Right-Hand-Side) assuming A.
        '''
        return self.rhsSubstitute(X, X)

    def deriveLeftViaEquivalence(self):
        '''
        From A = B, derive A (the Right-Hand-Side) assuming B.
        '''
        return self.lhsSubstitute(X, X)
    
    def deduceInBool(self):
        '''
        Deduce and return that this equality statement is in the set of BOOLEANS.
        '''
        from axioms import equalityInBool
        return equalityInBool.specialize({x:self.lhs, y:self.rhs})
    
    def inBoolViaBooleanEquality(self):
        '''
        From A=TRUE, A=FALSE, TRUE=A, or FALSE=A, derive and return inBool(A).
        '''
        from proveit.logic import TRUE, FALSE
        from proveit.logic.boolean.theorems import inBoolIfEqTrue, inBoolIfEqTrueRev, inBoolIfEqFalse, inBoolIfEqFalseRev
        if self.rhs == TRUE:
            return inBoolIfEqTrue.specialize({A:self.lhs}).deriveConclusion().proven({self})
        if self.lhs == TRUE:
            return inBoolIfEqTrueRev.specialize({A:self.rhs}).deriveConclusion().proven({self})
        if self.rhs == FALSE:
            return inBoolIfEqFalse.specialize({A:self.lhs}).deriveConclusion().proven({self})
        if self.lhs == FALSE:
            return inBoolIfEqFalseRev.specialize({A:self.rhs}).deriveConclusion().proven({self})
    
    def evaluate(self):
        '''
        Given operands that may be evaluated, derive and return this
        expression equated to TRUE or FALSE.  If both sides equate to
        the same, it will equate to TRUE.  Otherwise, it calls
        evalEquality using the evaluated left and right hand sides
        of the expression to determine the evaluation of the equality.
        '''
        from proveit.logic import TRUE
        from proveit.logic.boolean.boolOps import _evaluate
        def doEval():
            '''
            Performs the actual work if we can't simply look up the evaluation.
            '''
            if self.lhs == self.rhs:
                # simple case where both sides are the same, use reflexivity
                return Equals(self.concludeViaReflexivity(), TRUE).concludeBooleanEquality()
            
            # evaluate both sides and see if simplification is possible
            lhsSimpl = self.lhs
            rhsSimpl = self.rhs
            try:
                lhsEval = self.lhs.evaluate()
                lhsSimpl = lhsEval.rhs
            except AttributeError:
                lhsEval = None
            try:
                rhsEval = self.rhs.evaluate()
                rhsSimpl = rhsEval.rhs
            except AttributeError:
                rhsEval = None
    
            if lhsEval is None and rhsEval is None:
                # Cannot simplify further.  Use evalEquality.
                return lhsSimpl.evalEquality(rhsSimpl)
            else:         
                # evaluate the simplified version
                simplEval = Equals(lhsSimpl, rhsSimpl).evaluate()
                val = simplEval.rhs
                # Using substitution, go from simplEval to self=val
                if lhsEval is not None:
                    lhsEval.lhsSubstitute(Equals(Equals(X, rhsSimpl), val), X)
                if rhsEval is not None:
                    rhsEval.lhsSubstitute(Equals(Equals(self.lhs, X), val), X)
                return Equals(self, val)
            
        return _evaluate(self, doEval)
        

def _autoSub(outcome, outerExpr, superExpr, subExpr, eqGenMethodName, eqGenMethodArgs=None, eqGenKeywordArgs=None, criteria=None, subExprClass=None, suppressWarnings=False):
    if eqGenMethodArgs is None: eqGenMethodArgs = []
    if eqGenKeywordArgs is None: eqGenKeywordArgs = dict()
    meetsCriteria = (subExprClass is None or isinstance(subExpr, subExprClass)) and \
        (criteria is None or criteria(subExpr))
    if meetsCriteria and hasattr(subExpr, eqGenMethodName):
        generatedEquality = None
        try:
            generatedEquality = getattr(subExpr, eqGenMethodName)(*eqGenMethodArgs, **eqGenKeywordArgs)
        except Exception as e:
            if not suppressWarnings:
                print "Warning, failure in autosub attempt when applying '" + eqGenMethodName + "' method to " + str(subExpr) + ":"
                print e
                print "Continuing on"
            
        if generatedEquality is not None and isinstance(generatedEquality, Equals) and (generatedEquality.lhs == subExpr or generatedEquality.rhs == subExpr):
            if superExpr == outerExpr:
                # substitute all occurences
                fnExpr, fnArgs = outerExpr, None 
            else:
                # substitute only occurences within superExpr
                subbing = generatedEquality.lhs if generatedEquality.lhs == subExpr else generatedEquality.rhs
                replacement = generatedEquality.rhs if generatedEquality.lhs == subExpr else generatedEquality.lhs
                fnExpr, fnArgs = generatedEquality._subFn(superExpr, None, subbing, replacement)
                fnExpr = outerExpr.substituted({superExpr:fnExpr})
            if outcome == 'substitution':
                return generatedEquality.substitution(fnExpr, fnArgs)
            elif generatedEquality.lhs == subExpr:
                if outcome == 'substitute':
                    return generatedEquality.rhsSubstitute(fnExpr, fnArgs)
                elif outcome == 'statement_substitution':
                    return generatedEquality.rhsStatementSubstitute(fnExpr, fnArgs)
            elif generatedEquality.rhs == subExpr:
                if outcome == 'substitute':
                    return generatedEquality.lhsSubstitute(fnExpr, fnArgs)
                elif outcome == 'statement_substitution':
                    return generatedEquality.lhsStatementSubstitute(fnExpr, fnArgs)
    for subExpr in subExpr.subExprGen():
        result = _autoSub(outcome, outerExpr, superExpr, subExpr, eqGenMethodName, eqGenMethodArgs, eqGenKeywordArgs, criteria, subExprClass, suppressWarnings)
        if result is not None: return result
    return None            
    
def autoSubstitute(expr, eqGenMethodName, eqGenMethodArgs=None, eqGenKeywordArgs=None, criteria=None, subExprClass=None, superExpr=None, suppressWarnings = False):
    '''
    From a given expr = P(x), derives and returns some P(y) via some x=y that is generated by
    calling a method of the name eqGenMethodName on one of its sub-expressions.  eqGenMethodArgs
    and eqGenKeywordArgs may be a list of arguments and/or a dictionary of keyword arguments
    respectively to pass on to the eqGenMethodName method.  If provided, criteria, subExprClass,
    and superExpr will force selectivity in choosing the sub-expression to generate x=y.
    Specificially the sub-expression must be a sub-expression of superExpr (if provided)
    beyond being a sub-expression of expr, it must be an instance of subExprClass (if provided), 
    and the criteria method (if provide) must return true when passed in the sub-expression.
    If superExpr is provided, replacements are only made within superExpr.
    '''
    if superExpr is None: superExpr = expr
    return _autoSub('substitute', expr, superExpr, superExpr, eqGenMethodName, eqGenMethodArgs, eqGenKeywordArgs, criteria, subExprClass, suppressWarnings)

def autoSubstitution(expr, eqGenMethodName, eqGenMethodArgs=None, eqGenKeywordArgs=None, criteria=None, subExprClass=None, superExpr=None, suppressWarnings = False):
    '''
    From a given expr = f(x), derives and returns some f(x) = f(y) via some x=y that is generated by
    calling a method of the name eqGenMethodName on one of its sub-expressions.  eqGenMethodArgs
    and eqGenKeywordArgs may be a list of arguments and/or a dictionary of keyword arguments
    respectively to pass on to the eqGenMethodName method.  If provided, criteria, subExprClass,
    and superExpr will force selectivity in choosing the sub-expression to generate x=y.
    Specificially the sub-expression must be a sub-expression of superExpr (if provided)
    beyond being a sub-expression of expr, it must be an instance of subExprClass (if provided), 
    and the criteria method (if provide) must return true when passed in the sub-expression.
    If superExpr is provided, replacements are only made within superExpr.
    '''
    if superExpr is None: superExpr = expr
    return _autoSub('substitution', expr, superExpr, superExpr, eqGenMethodName, eqGenMethodArgs, eqGenKeywordArgs, criteria, subExprClass, suppressWarnings)

def autoStatementSubstitution(expr, eqGenMethodName, eqGenMethodArgs=None, eqGenKeywordArgs=None, criteria=None, subExprClass=None, superExpr=None, suppressWarnings = False):
    '''
    From a given expr = P(x), derives and returns some P(x) => P(y) via some x=y that is 
    generated by calling a method of the name eqGenMethodName on one of its sub-expressions.
    eqGenMethodArgs and eqGenKeywordArgs may be a list of arguments and/or a dictionary of 
    keyword arguments respectively to pass on to the eqGenMethodName method.  If provided, 
    criteria, subExprClass, and superExpr will force selectivity in choosing the sub-expression 
    to generate x=y.  Specificially the sub-expression must be a sub-expression of superExpr 
    (if provided) beyond being a sub-expression of expr, it must be an instance of subExprClass 
    (if provided), and the criteria method (if provide) must return true when passed in the 
    sub-expression. If superExpr is provided, replacements are only made within superExpr.
    '''
    if superExpr is None: superExpr = expr
    return _autoSub('statement_substitution', expr, superExpr, superExpr, eqGenMethodName, eqGenMethodArgs, eqGenKeywordArgs, criteria, subExprClass, suppressWarnings)        

def generateSubExpressions(expr, criteria=None, subExprClass=None):
    meetsCriteria = (subExprClass is None or isinstance(expr, subExprClass)) and \
        (criteria is None or criteria(expr))
    if meetsCriteria: yield expr
    for subExpr in expr.subExprGen():
        for subSubExpr in generateSubExpressions(subExpr, criteria, subExprClass):
            yield subSubExpr

def extractSubExpr(expr, criteria=None, subExprClass=None):
    for subExpr in generateSubExpressions(expr, criteria=criteria, subExprClass=subExprClass):
        return subExpr
    print "Sub expression meeting the criteria not found"
