from proveit import Function, Literal
from proveit import equality_prover, ClassMembership
from proveit import f, A, B

class IsGridGraph(ClassMembership):
    '''
    IsGridGraph(G) is the class predicate claim that G is a grid graph,
    and replaces the problematic conceptual approach of claiming that
    "G is in the class of Grid Graphs".

    UNDER CONSTRUCTION.

    See the IsGraph() class predicate for analogous but more general
    class dealing with graphs more generally and for comments about
    the conceptualization of a graph.
    '''
    _operator_ = Literal('IsGridGraph', r'\textrm{IsGridGraph}',
                         theory=__file__)
    
    def __init__(self, G, *, styles=None):
        ClassMembership.__init__(self, IsGridGraph._operator_,
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
            return r'{\textrm{GridGraphs}}'
        return r'GridGraphs'

    # Kept here temporarily as a model
    # @equality_prover('defined', 'define')
    # def definition(self, **defaults_config):
    #     '''
    #     Prove that
    #     IsSurjection(f, A, B) =
    #     IsFunction(f, A, B) and Image(f, A) = B

    #     for the f, A, and B in correspondence with this
    #     InjectionsMembership.
    #     '''
    #     from . import is_surjection_def
    #     _A = self.domain
    #     _B = self.codomain
    #     _f = self.element
    #     return is_surjection_def.instantiate(
    #             {A:_A, B:_B, f:_f}, auto_simplify=False)

    # Kept here temporarily as a model
    # def as_defined(self):
    #     '''
    #     From self=IsSurjection(f, A, B), return
    #     IsFunction(f, A, B) and Image(f, A) = B
    #     '''
    #     from proveit.logic import And, Equals, IsFunction, Image
    #     _f = self.element
    #     _A, _B = self.domain, self.codomain
    #     return And(IsFunction(_f, _A, _B), Equals(Image(_f, _A), _B))
