from proveit import Function, Literal
from proveit import equality_prover, ClassMembership
from proveit import f, A, B

class IsGraph(ClassMembership):
    '''
    IsGraph(G) is the class predicate claim that G is a graph, and
    replaces the problematic conceptual approach of claiming that
    "G is in the class of Graphs".
    For our purposes here, class of graphs includes both
    finite and infinite graphs, but is initially conceptualized as
    the class of simple graphs (i.e. no loops and no parallel edges).
    The claim IsGraph(G) then is tantamount to claiming that G is
    an ordered pair (V, E) of vertices V and edges E such that
    E is a subset of the set of 2-element subsets of V.
    '''
    _operator_ = Literal('IsGraph', r'\textrm{IsGraph}',
                         theory=__file__)
    
    def __init__(self, G, *, styles=None):
        ClassMembership.__init__(self, IsGraph._operator_,
                                 G, styles=styles)
        self.graph = G

    # def formatted_class(self, format_type):
    #     formatted_domain = self.domain.formatted(format_type, fence=True)
    #     formatted_codomain = self.codomain.formatted(format_type, fence=True)
    #     if format_type == 'latex':
    #         return (r'\left[' + formatted_domain 
    #                 + r' \xrightarrow[\text{onto}]{} '
    #                 + formatted_codomain + r'\right]')
    #     else:
    #         return ('[' + formatted_domain + r' ->onto '
    #                 + formatted_codomain + r']')

    def formatted_class(self, format_type):
        if format_type == 'latex':
            return r'{\textrm{Graphs}}'
        return r'Graphs'

    @equality_prover('defined', 'define')
    def definition(self, **defaults_config):
        '''
        Prove that
        IsSurjection(f, A, B) =
        IsFunction(f, A, B) and Image(f, A) = B

        for the f, A, and B in correspondence with this
        InjectionsMembership.
        '''
        from . import is_surjection_def
        _A = self.domain
        _B = self.codomain
        _f = self.element
        return is_surjection_def.instantiate(
                {A:_A, B:_B, f:_f}, auto_simplify=False)

    def as_defined(self):
        '''
        From self=IsSurjection(f, A, B), return
        IsFunction(f, A, B) and Image(f, A) = B
        '''
        from proveit.logic import And, Equals, IsFunction, Image
        _f = self.element
        _A, _B = self.domain, self.codomain
        return And(IsFunction(_f, _A, _B), Equals(Image(_f, _A), _B))
