from proveit._core_.expression.expr import Expression
import re

class Label(Expression):
    """
    Label is the base class for the Variable, Literal, and MultiVariable expr
    classes (Label is not itself an expr class).  It is a mathematical label
    with string and latex formatting.
    """
    def __init__(self, stringFormat, latexFormat=None, labelType = 'Label', extraCoreInfo = tuple(), subExpressions=tuple()):
        '''
        Create a Label with the given string and latex formatting.
        By default, the latex formatting is the same as the string formatting.
        '''
        self.stringFormat = stringFormat
        if latexFormat is None: latexFormat = stringFormat
        self.latexFormat = latexFormat.strip() if latexFormat is not None else stringFormat
        assert re.match('[!-~]+', self.stringFormat), 'Label stringFormat may include only printable ascii characters and no space'
        assert re.match('[ -~]+', self.latexFormat), 'Label latexFormat may include only printable ascii characters'
        if not isinstance(self.stringFormat, str):
            raise TypeError("'stringFormat' must be a str")
        if not isinstance(self.latexFormat, str):
            raise TypeError("'latexFormat' must be a str")
        if ',' in self.stringFormat or ',' in self.latexFormat:
            raise ValueError("Comma not allowed within a label's formatting")
        coreInfo = [labelType] + self._labelInfo() + list(extraCoreInfo)
        Expression.__init__(self, coreInfo, subExpressions=subExpressions)
        
    def string(self, **kwargs):
        '''
        Return a string representation of the Label.
        '''
        return self.stringFormat

    def latex(self, **kwargs):
        '''
        Return a latex representation of the Label.
        '''
        return self.latexFormat

    def _labelInfo(self):
        '''
        Return the Label's info to be used in the expr's core info.
        '''
        return [self.stringFormat, self.latexFormat]    
    
    @classmethod
    def _make(labelClass, coreInfo, styles, subExpressions):
        if len(subExpressions) > 0:
            raise ValueError('Not expecting any subExpressions of Label')
        if len(coreInfo) != 3:
            raise ValueError("Expecting " + labelClass.__name__ + " coreInfo to contain 3 items: '" + labelClass.__name + "', stringFormat, and latexFormat")
        if coreInfo[0] != labelClass.__name__:
            raise ValueError("Expecting coreInfo[0] to be '" + labelClass.__name__ + "'")
        return labelClass(coreInfo[1], coreInfo[2]).withStyles(**styles)

    def remakeArguments(self):
        '''
        Yield the argument values that could be used to recreate the 
        Label.  This is a default for simple Labels, Variables, or Literals.
        '''
        import inspect
        init_args = inspect.getargspec(self.__class__.__init__)[0]
        if len(init_args)==1:
            return # no arguments (except self) are taken
        if len(init_args)>=3 and init_args[1]=='stringFormat' and init_args[2]=='latexFormat':
            stringFormat, latexFormat = self.coreInfo()[1:3]
            yield '"' + stringFormat + '"'
            if latexFormat != stringFormat:
                yield ('latexFormat', 'r"' + latexFormat + '"')
        else:
            raise LabelError("Must properly implement the 'remakeArguments' method for class %s"%str(self.__class__))

class LabelError:
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg