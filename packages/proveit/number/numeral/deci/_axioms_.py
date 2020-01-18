import sys
from proveit._core_.context import Axioms
sys.modules[__name__] = Axioms(__name__, __file__)
