import sys
from proveit._core_.context import CommonExpressions
sys.modules[__name__] = CommonExpressions(__name__, __file__)
