import math

symbol_table = {}

class Expression:
    def __init__(self, tag, args):
        self.tag = tag
        self.args = args
        
    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False
            
        return type(self.tag) == type(other.tag) and self.tag == other.tag and self.args == other.args
        
    def substitute(self, expr1, expr2):
        if self == expr1:
            return expr2
        else:
            return Expression(self.tag, [arg.substitute(expr1, expr2) for arg in self.args])
        
    def evaluate(self):
        if self.is_number():
            return self
        if self.is_symbol():
            val = symbol_table.get(self.tag)
            return self if val == None else val
        
        # Non standard evaluation
        if self.tag == "If" and len(self.args) == 3:
            cond = self.args[0].evaluate()
            if cond == Expression("True", []):
                return self.args[1].evaluate()
            elif cond == Expression("False", []):
                return self.args[2].evaluate()
            else:
                return Expression('If', [cond] + self.args[1:])
        elif self.tag == 'Set' and len(self.args) == 2 and self.args[0].is_symbol():
            arg_ev = self.args[1].evaluate()
            symbol_table[self.args[0].tag] = arg_ev
            return arg_ev
            
        elif self.tag == 'Function' and len(self.args) == 2:
            return self
            
        # Standard evaluation -- first evaluate arguments
        args_ev = [arg.evaluate() for arg in self.args]
        
        if self.tag == 'Plus':
            if all([arg.is_number() for arg in args_ev]):
                return Expression(sum(arg.tag for arg in args_ev), [])
        elif self.tag == 'Times':
            if all([arg.is_number() for arg in args_ev]):
                return Expression(math.prod(arg.tag for arg in args_ev), [])
        elif self.tag == 'Equals' and len(args_ev) == 2:
            if args_ev[0] == args_ev[1]:
                return Expression('True', [])
            else:
                return Expression('False', [])
        elif self.tag == 'Apply':
            return self.args[0].args[1].substitute(self.args[0].args[0], self.args[1]).evaluate() 
        
        return Expression(self.tag, args_ev)
        
    def is_number(self):
        return type(self.tag) != str
        
    def is_symbol(self):
        return type(self.tag) == str and self.args == []
        
    def __repr__(self):
        if self.is_number():
            return str(self.tag)
            
        if self.is_symbol():
            return self.tag
            
        return self.tag + '[' + ','.join([arg.__repr__() for arg in self.args]) + ']'

        
def parse(s):
    if '[' not in s:
        if '.' in s:
            return Expression(float(s), [])
        if s[0] in '0123456789':
            return Expression(int(s), [])
        # s represents a symbol
        return Expression(s, [])
        
    # compound case
    i = s.find('[')
    return  Expression(s[:i], parse_comma(s[i+1:-1]))
 
    
    

def parse_comma(s):
    if s == '':
        return []
        
    openings = 0
    closings = 0
    for i, c in enumerate(s):
        if c == '[':
            openings += 1
        elif c == ']':
            closings += 1
        elif c == ',' and openings == closings:
            return [parse(s[:i])] + parse_comma(s[i+1:])
            
    return [parse(s)]

while True:
    expr =parse(input('ENSEA>>> '))
    print(expr.evaluate())
