from proveit import USE_DEFAULTS, maybeFencedString
from proveit._common_ import a
from proveit.number.sets.number_set import NumberSet

class RealsSet(NumberSet):
    def __init__(self):
        NumberSet.__init__(self, 'Reals',r'\mathbb{R}', context=__file__)

    def deduceMembershipInBool(self, member):
        from ._theorems_ import xInRealsInBool
        from proveit._common_ import x
        return xInRealsInBool.specialize({x:member})
    
class RealsPosSet(NumberSet):
    def __init__(self):
        NumberSet.__init__(self, 'RealsPos', r'\mathbb{R}^+', context=__file__)
    
    def deduceMemberLowerBound(self, member, assumptions=USE_DEFAULTS):
        from real.theorems import inRealsPos_iff_positive
        return inRealsPos_iff_positive.specialize({a:member},assumptions=assumptions).deriveRightImplication(assumptions)   
    
    def string(self, **kwargs):
        inner_str = NumberSet.string(self, **kwargs)
        # only fence if forceFence=True (nested exponents is an example of when fencing must be forced)
        kwargs['fence'] = kwargs['forceFence'] if 'forceFence' in kwargs else False        
        return maybeFencedString(inner_str, **kwargs)

    def latex(self, **kwargs):
        inner_str = NumberSet.latex(self, **kwargs)
        # only fence if forceFence=True (nested exponents is an example of when fencing must be forced)
        kwargs['fence'] = kwargs['forceFence'] if 'forceFence' in kwargs else False        
        return maybeFencedString(inner_str, **kwargs)

    def deduceMembershipInBool(self, member):
        from ._theorems_ import xInRealsPosInBool
        from proveit._common_ import x
        return xInRealsPosInBool.specialize({x:member})
            
class RealsNegSet(NumberSet):
    def __init__(self):
        NumberSet.__init__(self, 'RealsNeg', r'\mathbb{R}^-', context=__file__)
    
    def deduceMemberUpperBound(self, member, assumptions=USE_DEFAULTS):
        from real.theorems import inRealsNeg_iff_negative
        return inRealsNeg_iff_negative.specialize({a:member},assumptions=assumptions).deriveRightImplication(assumptions)    
    
    def string(self, **kwargs):
        inner_str = NumberSet.string(self, **kwargs)
        # only fence if forceFence=True (nested exponents is an example of when fencing must be forced)
        kwargs['fence'] = kwargs['forceFence'] if 'forceFence' in kwargs else False        
        return maybeFencedString(inner_str, **kwargs)

    def latex(self, **kwargs):
        inner_str = NumberSet.latex(self, **kwargs)
        # only fence if forceFence=True (nested exponents is an example of when fencing must be forced)
        kwargs['fence'] = kwargs['forceFence'] if 'forceFence' in kwargs else False        
        return maybeFencedString(inner_str, **kwargs)

    def deduceMembershipInBool(self, member):
        from ._theorems_ import xInRealsNegInBool
        from proveit._common_ import x
        return xInRealsNegInBool.specialize({x:member})

try:
    # Import some fundamental axioms and theorems without quantifiers.
    # Fails before running the _axioms_ and _theorems_ notebooks for the first time, but fine after that.
    from ._theorems_ import realsPosInReals, realsNegInReals, intsInReals, natsInReals, natsPosInReals
except:
    pass
