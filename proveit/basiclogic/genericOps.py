from proveit.expression import Operation, Lambda, STRING, LATEX
from proveit.multiExpression import multiExpression
from proveit.everythingLiteral import EVERYTHING

class BinaryOperation(Operation):
    def __init__(self, operator, A, B):
        Operation.__init__(self, operator, (A, B))
        self.leftOperand = A
        self.rightOperand = B
        
    def formatted(self, formatType, fence=False, subLeftFence=True, subRightFence=True):
        # override this default as desired
        formattedLeft = self.leftOperand.formatted(formatType, fence=subLeftFence)
        formattedRight = self.rightOperand.formatted(formatType, fence=subRightFence)
        formattedOp = self.operator.formatted(formatType)
        innerStr = formattedLeft + ' ' + formattedOp + ' ' + formattedRight
        if fence:
            if formatType == LATEX:
                return r'\left(' + innerStr + r'\right)'
            else:
                return '(' + innerStr + ')'
        else: return innerStr

class AssociativeOperation(Operation):
    def __init__(self, operator, *operands):
        '''
        Represent an associative operator operating on any number of operands.
        '''
        Operation.__init__(self, operator, operands)   
        # What is the sound of one (or no) hand clapping?  Who really cares?
        if len(self.operands) < 2:
            raise ValueError("An AssociativeOperation must have at least 2 operands")  
    
    def formatted(self, formatType, fence=False, subFence=True):
        '''
        Format the associative operation in the form "A * B * C" where '*' is a stand-in for
        the operator that is obtained from self.operator.formatted(formatType).
        '''
        outStr = ''
        formattedOperands = [operand.formatted(formatType, fence=subFence) for operand in self.operands]
        if formatType == STRING:
            if fence: outStr += '('
            outStr += (' ' + self.operator.formatted(formatType) + ' ').join(formattedOperands)
            if fence: outStr += ')'
        elif formatType == LATEX:
            if fence: outStr += r'\left('
            outStr += (' ' + self.operator.formatted(formatType) + ' ').join(formattedOperands)
            if fence: outStr += r'\right)'
        return outStr           

class OperationOverInstances(Operation):
    def __init__(self, operator, instanceVars, instanceExpr, domain=EVERYTHING, conditions=tuple()):
        '''
        Create an Operation for the given operator over instances of the given instance Variables,
        instanceVars, for the given instance Expression, instanceExpr under the given conditions
        and/or with instance variables restricted to the given domain.
        That is, the operation operates over all possibilities of given Variable(s) wherever
        the condition(s) is/are satisfied.  Examples include forall, exists, summation, etc.
        instanceVars and conditions may be singular or plural (iterable).
        Internally, this is represented as an Operation whose etcExpr is in the following form
        (where '->' represents a Lambda and {...} represents an ExpressionDict):
          {'instance_mapping' : instanceVars -> {'expression':instanceExpr, 'conditions':conditions}, 'domain':domain}
        '''
        Operation.__init__(self, operator, OperationOverInstances._createOperand(instanceVars, instanceExpr, domain, conditions))
        params = OperationOverInstances.extractParameters(self.operands)
        self.instanceVars = params['instanceVars']
        self.instanceExpr = params['instanceExpr']
        self.domain = params['domain']
        self.conditions = params['conditions']
    
    @staticmethod
    def _createOperand(instanceVars, instanceExpr, domain, conditions):
        lambdaFn = Lambda(instanceVars, {'instance_expression':instanceExpr, 'conditions':multiExpression(conditions)})
        return {'instance_mapping':lambdaFn, 'domain':domain}
    
    @staticmethod
    def extractParameters(operands):
        '''
        Extract the parameters from the OperationOverInstances operands:
        instanceVars, instanceExpr, conditions, domain
        '''
        domain = operands['domain']
        lambdaFn = operands['instance_mapping']
        instanceVars = lambdaFn.arguments
        conditions = lambdaFn.expression['conditions']
        instanceExpr = lambdaFn.expression['instance_expression']
        return {'instanceVars':instanceVars, 'instanceExpr':instanceExpr, 'domain':domain, 'conditions':conditions}
        
    def implicitInstanceVars(self, formatType, overriddenImplicitVars = None):
        '''
        Return instance variables that need not be shown explicitly in the
        list of instance variables in the formatting.
        Use overriddenImplicitVars to declare extra implicit instance variables
        (all or just the overridden ones).
        '''
        return set() if overriddenImplicitVars is None else overriddenImplicitVars

    def implicitConditions(self, formatType):
        '''
        Returns conditions that need not be shown explicitly in the formatting.
        By default, this is empty (all conditions are shown).
        '''
        return set()

    def hasDomain(self):
        '''
        Returns True if this OperationOverInstances has a domain restriction.
        '''
        return self.domain != EVERYTHING
        
    def hasCondition(self):
        '''
        Returns True if this OperationOverInstances has conditions.
        '''
        return self.conditions is not None and len(self.conditions) > 0

    def formatted(self, formatType, fence=False):
        # override this default as desired
        implicitIvars = self.implicitInstanceVars(formatType)
        hasExplicitIvars = (len(implicitIvars) < len(self.instanceVars))
        implicitConditions = self.implicitConditions(formatType)
        hasExplicitConditions = self.hasCondition() and (len(implicitConditions) < len(self.conditions))
        outStr = ''        
        if formatType == STRING :
            if fence: outStr += '['
            outStr += self.operator.formatted(formatType) + '_{'
            if hasExplicitIvars:
                outStr += ', '.join([var.formatted(formatType) for var in self.instanceVars if var not in implicitIvars])
            if self.hasDomain():
                outStr += ' in ' if formatType == STRING else ' \in '
                outStr += self.domain.formatted(formatType, fence=True)
            if hasExplicitConditions:
                if hasExplicitIvars: outStr += " | "
                outStr += ', '.join(condition.formatted(formatType) for condition in self.conditions if condition not in implicitConditions) 
            outStr += '} ' + self.instanceExpr.formatted(formatType,fence=True)
            if fence: outStr += ']'
        if formatType == LATEX:
            if fence: outStr += r'\left['
            outStr += self.operator.formatted(formatType) + '_{'
            if hasExplicitIvars:
                outStr += ', '.join([var.formatted(formatType) for var in self.instanceVars if var not in implicitIvars])
            if self.hasDomain():
                outStr += ' in ' if formatType == STRING else ' \in '
                outStr += self.domain.formatted(formatType, fence=True)
            if hasExplicitConditions:
                if hasExplicitIvars: outStr += " | "
                outStr += ', '.join(condition.formatted(formatType) for condition in self.conditions if condition not in implicitConditions) 
            outStr += '} ' + self.instanceExpr.formatted(formatType,fence=True)
            if fence: outStr += r'\right]'

        return outStr        

    def instanceSubstitution(self, equivalenceForallInstances):
        '''
        Equate this OperationOverInstances, Upsilon_{..x.. in S | ..Q(..x..)..} f(..x..),
        with one that substitutes instance expressions given some 
        equivalenceForallInstances = forall_{..x.. in S | ..Q(..x..)..} f(..x..) = g(..x..).
        Derive and return the following type of equality assuming equivalenceForallInstances:
        Upsilon_{..x.. in S | ..Q(..x..)..} f(..x..) = Upsilon_{..x.. in S | ..Q(..x..)..} g(..x..)
        Works also when there is no domain S and/or no conditions ..Q...
        '''
        from proveit.basiclogic.axioms import instanceSubstitution
        from proveit.basiclogic import Forall, Equals
        from proveit.number import num
        from proveit.common import n, Qetc, xEtc, yEtc, zEtc, etc_QxEtc, f, g, fxEtc, fyEtc, gxEtc, gzEtc, Upsilon, S
        if not isinstance(equivalenceForallInstances, Forall):
            raise InstanceSubstitutionException("equivalenceForallInstances must be a forall expression", self, equivalenceForallInstances)
        if len(equivalenceForallInstances.instanceVars) != len(self.instanceVars):
            raise InstanceSubstitutionException("equivalenceForallInstances must have the same number of variables as the OperationOverInstances having instances substituted", self, equivalenceForallInstances)
        if equivalenceForallInstances.domain != self.domain:
            raise InstanceSubstitutionException("equivalenceForallInstances must have the same domain as the OperationOverInstances having instances substituted", self, equivalenceForallInstances)
        # map from the forall instance variables to self's instance variables
        iVarSubstitutions = {forallIvar:selfIvar for forallIvar, selfIvar in zip(equivalenceForallInstances.instanceVars, self.instanceVars)}
        if equivalenceForallInstances.conditions.substituted(iVarSubstitutions) != self.conditions:
            raise InstanceSubstitutionException("equivalenceForallInstances must have the same conditions as the OperationOverInstances having instances substituted", self, equivalenceForallInstances)
        if not isinstance(equivalenceForallInstances.instanceExpr, Equals):
            raise InstanceSubstitutionException("equivalenceForallInstances be an equivalence within Forall: " + str(equivalenceForallInstances))
        if equivalenceForallInstances.instanceExpr.lhs.substituted(iVarSubstitutions) != self.instanceExpr:
            raise InstanceSubstitutionException("lhs of equivalence in equivalenceForallInstances must match the instance expression of the OperationOverInstances having instances substituted", self, equivalenceForallInstances)
        return instanceSubstitution.specialize({n:num(len(self.instanceVars)), Upsilon:self.operator, xEtc:self.instanceVars, yEtc:self.instanceVars, zEtc:self.instanceVars, \
                                                etc_QxEtc:self.conditions, S:self.domain, fxEtc:self.instanceExpr, gxEtc:equivalenceForallInstances.instanceExpr.rhs.substituted(iVarSubstitutions)})

    def substituteInstances(self, equivalenceForallInstances):
        '''
        Assuming this OperationOverInstances, Upsilon_{..x.. in S | ..Q(..x..)..} f(..x..)
        to be a true statement, derive and return Upsilon_{..x.. in S | ..Q(..x..)..} g(..x..)
        given some equivalenceForallInstances = forall_{..x.. in S | ..Q(..x..)..} f(..x..) = g(..x..).
        Works also when there is no domain S and/or no conditions ..Q...
        '''
        substitution = self.instanceSubstitution(equivalenceForallInstances)
        return substitution.deriveRightViaEquivalence()
        
class InstanceSubstitutionException(Exception):
    def __init__(self, msg, operationOverInstances, equivalenceForallInstances):
        self.msg = msg
        self.operationOverInstances = operationOverInstances
        self.equivalenceForallInstances = equivalenceForallInstances
    def __str__(self):
        return self.msg + '.\n  operationOverInstances: ' + str(self.operationOverInstances) + '\n  equivalenceForallInstances: ' + str(self.equivalenceForallInstances)