# GuestOS structures emulator

def comment(text, width=80):
    print('#' * (width - len(text) - 1) + ' ' + text)
# comment('computation', 60)


################################################################# system modules


import os, sys


################################################################ base node class

class Object:

    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.val = V
        self.slot = {}
        self.nest = []
        self.sid = id(self)

    ################################################## text dump

    def __repr__(self): return self.dump()

    def dump(self, depth=0, prefix=''):
        tree = self.pad(depth) + self.head(prefix)
        for i in self.slot:
            tree += self.slot[i].dump(depth + 1, prefix='%s = ' % i)
        idx = 0
        for j in self.nest:
            tree += j.dump(depth + 1, prefix='%s = ' % idx)
            idx += 1
        return tree

    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self._val(), self.sid)

    def pad(self, depth):
        return '\n' + '\t' * depth

    def _val(self):
        return '%s' % self.val

    ################################################## operators

    def __getitem__(self, key):
        return self.slot[key]

    def __setitem__(self, key, that):
        self.slot[key] = that
        return self

    def __lshift__(self, that):
        return self.__setitem__(that.type, that)

    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    def __floordiv__(self, that):
        self.nest.append(that)
        return self

    ########################################### stack operations

    ################################################ computation

    def eval(self, ctx):
        raise TypeError(Error('eval') // self // ctx)

    def apply(self, that, ctx):
        raise TypeError(Error('apply') // self // that // ctx)


############################################################### error processing


class Error(Object):
    pass

##################################################################### primitives

class Primitive(Object):
    def eval(self, env): return self

class Symbol(Primitive):
    def eval(self, env): return env[self.val]

class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))

    def _val(self): return hex(self.val)

class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))

    def _val(self): return bin(self.val)

################################################################ executable data

class Active(Object):
    def eval(self, ctx): return self

class Operator(Active):
    def eval(self, ctx):
        if self.val == '//':
            return self.nest[0].eval(ctx) // self.nest[1].eval(ctx)
        elif self.val == '<<':
            return self.nest[0].eval(ctx) << self.nest[1].eval(ctx)
        elif self.val == '>>':
            return self.nest[0].eval(ctx) >> self.nest[1].eval(ctx)
        elif self.val == '`':
            return self.nest[0] # quote unevaluated
        else:
            return Active.eval(self, ctx)

class VM(Active):
    pass


vm = VM('metaL')

########################################################################## lexer


import ply.lex as lex

tokens = ['symbol', 'number', 'integer', 'hex', 'bin',
          'push', 'lshift', 'rshift', 'tick']

t_ignore = ' \t\r'
t_ignore_comment = '\#.*'

def t_nl(t):
    r'\n'
    t.lexer.lineno += 1

def t_tick(t):
    r'`'
    t.value = Operator(t.value)
    return t
def t_push(t):
    r'//'
    t.value = Operator(t.value)
    return t
def t_lshift(t):
    r'<<'
    t.value = Operator(t.value)
    return t
def t_rshift(t):
    r'>>'
    t.value = Operator(t.value)
    return t

def t_number_exp(t):
    r'[+\-]?[0-9]+[eE][+\-]?[0-9]+'
    t.value = Number(t.value)
    t.type = 'number'
    return t
def t_number_dot(t):
    r'[+\-]?[0-9]+\.[0-9]+'
    t.value = Number(t.value)
    t.type = 'number'
    return t
def t_hex(t):
    r'0x[0-9a-fA-F]+'
    t.value = Hex(t.value)
    return t
def t_bin(t):
    r'0b[01]+'
    t.value = Bin(t.value)
    return t
def t_integer(t):
    r'[+\-]?[0-9]+'
    t.value = Integer(t.value)
    return t

def t_symbol(t):
    r'[^ \t\r\n\#]+'
    t.value = Symbol(t.value)
    return t

def t_ANY_error(t): raise SyntaxError(t)


lexer = lex.lex()

######################################################################### parser
#################################################################### interpreter

import ply.yacc as yacc

precedence = (
    ('left', 'push',),
    ('left', 'lshift', 'rshift'),
    ('nonassoc', 'tick'),
)

def p_REPL_none(p):
    ' REPL : '
def p_REPL_loop(p):
    ' REPL : REPL ex '
    print(p[2])
    print(p[2].eval(vm))
    print(vm)
    print('-' * 66)

def p_ex_symbol(p):
    ' ex : symbol '
    p[0] = p[1]
def p_ex_number(p):
    ' ex : number '
    p[0] = p[1]
def p_ex_integer(p):
    ' ex : integer '
    p[0] = p[1]
def p_ex_hex(p):
    ' ex : hex '
    p[0] = p[1]
def p_ex_bin(p):
    ' ex : bin '
    p[0] = p[1]

def p_ex_tick(p):
    ' ex : tick ex '
    p[0] = p[1] // p[2]
def p_ex_push(p):
    ' ex : ex push ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_lshift(p):
    ' ex : ex lshift ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_rshift(p):
    ' ex : ex rshift ex '
    p[0] = p[2] // p[1] // p[3]

def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)


#################################################################### system init

if __name__ == '__main__':
    for srcfile in sys.argv[1:]:
        with open(srcfile) as src:
            parser.parse(src.read())
