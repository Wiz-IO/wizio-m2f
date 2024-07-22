# Copyright 2024 WizIO ( Georgi Angelov )
import os, sys, inspect, re, glob, itertools, time
from os.path import join, exists, basename, dirname
from typing import Dict, List, Tuple, Union, Callable, Any, Type
from functools import partial
from pathlib import Path

def ERROR(txt = ''):
    time.sleep(.1)
    txt = 'in %s() %s: ' % (inspect.stack()[1][3], txt)
    print( '\n[ERROR] %s\n' % txt)
    time.sleep(.1)
    sys.exit(-1)

#################################################

LIMIT = 50 # max recursion

ESC_ENTER = '®' # used only in macros
ESC_QUOTE = '©' # false quotes, protect comma

#################################################
# MK FUNCTIONS
#################################################

def split_percent(s):
    assert isinstance(s,str), type(s)
    idx = -1
    while 1:
        try:
            idx = s.index('%', idx+1)
        except ValueError:
            return None

        if idx > 0 and s[idx-1] == '\\' and not (idx > 1 and s[idx-2] == '\\'):
            continue

        return s[ : idx ], s[ idx + 1 : ]

def wildcard_match_list(pattern_list, target_list, negate=False):
    # first arg must be a list, not an iterable, because we use it twice
    assert isinstance(pattern_list, list), type(pattern_list)

    # pre-calculate all the patterns
    p_list = [ split_percent(p) for p in pattern_list ]

    for t in target_list:
        for p,pattern in zip(p_list, pattern_list):
            #print(t,p,pattern)
            if p is None:
                # no '%' so just a string compare
                flag = t == pattern
            else:
                flag = t.startswith(p[0]) and t.endswith(p[1])

            #print(flag,negate,flag^negate)
            # flag==True    => match
            # flag==False   => no-match
            # negate==False => filter
            # negate==True  => filter-out
            #
            #     flag  negate    desired result
            #   +------------------------------
            #   | true   true     false  (match + filter-out)
            #   | true   false    true   (no match + filter-out)
            #   | false  true     true   (match + filter)
            #   | false  false    false  (no match + filter)

            if flag:
                # quit searching on first match (only one match per target)
                if not negate:
                    # if we're filter then we return this target
                    # if we're filter-out then we skip this target
                    yield t
                break

        else:
            # at this point, none of the patterns matched
            if negate:
                yield t

def wildcard_replace(search, replace, text_list):

    s = split_percent(search) # %

    if s is None:
        assert 0
        return [replace if search==word else word for word in text_list]

    r = split_percent(replace) # %

    new_list = []
    for word in text_list:
        if word.startswith(s[0]) and word.endswith(s[1]):
            if r is None:
                new_list.append(replace)
            else:
                mid = word[len(s[0]) : len(word)-len(s[1])]
                new = r[0] + mid + r[1]
                new_list.append(new)
        else:
            new_list.append(word)

    return new_list

def flatten(list_of_lists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(list_of_lists)

def convert_to_unix_path(p):
    if os.name == 'nt':
        path = Path(p)
        parts = path.parts
        drive = parts[0][0].lower()
        unix_path = f"/{drive}/" + "/".join(parts[1:])
        return unix_path
    return p

def convert_to_win_path(p):
    if p[1] == ':':
        return p
    p = p.strip()
    if p.startswith('/'):
        p = p[1:]
    if p[1] == '/':
        drive, rest_of_path = p.split('/', 1)
        win_path = f'{drive.upper()}:/{rest_of_path}'
    else:
        win_path = p
    return win_path

def CLEAN(s):
    return s.replace(ESC_QUOTE, '')

def RESULT(s):
    # protect value
    return '©%s©'%CLEAN(s)

def SPLIT(s, delimiter, maxsplit=0):
    # protect delimiter: 'a,©boo,foo©,©,©' --> ['a', 'boo,foo', ',']
    pattern = r'' + delimiter + r'(?=(?:[^©]*©[^©]*©)*[^©]*$)'
    return re.split(pattern, s, maxsplit)

#################################################

def Dump(env, arg):
    # used only for debug
    env.dump()
    return ''

def BadArgument(e, arg):
    # $(function,)
    return ''

def Info(env, arg):
    # used only for debug
    print('<%s>' % CLEAN( env.subst(arg) ).replace(ESC_ENTER, '\n'))
    return ''

def Echo(e, arg):  return Info(e, arg)

def And(e, arg):
    # $(and condition1[,condition2[,condition3...]])
    A = SPLIT(arg, ',')
    for a in A:
        last = a = CLEAN( e.subst(a) )
        if not len( a.strip() ):
            return ''
    return RESULT( last.lstrip() )

def Or(e, arg):
    # $(or condition1[,condition2[,condition3...]])
    A = SPLIT(arg, ',')
    for a in A:
        a = CLEAN( e.subst(a) )
        if len( a.strip() ):
            return RESULT( a.lstrip() )
    return ''

def Strip(e, arg):
    # $(strip string)
    A   = CLEAN( e.subst(arg) ).split()
    res = ' '.join( [ a.strip() for a in A ] )
    return RESULT(res)

def Sort(e, arg):
    # $(sort list)
    A   = CLEAN( e.subst(arg) ).split()
    res = " ".join( sorted( set( A ) ) )
    return RESULT(res)

def Filter(e, arg, F = False):
    # $(filter pattern...,text)
    A = SPLIT(arg, ',', 1)
    pattern = CLEAN( e.subst(A[0]) ).split()
    text    = CLEAN( e.subst(A[1]) ).split()
    res     = " ".join( wildcard_match_list( pattern, text, F ) )
    return RESULT(res)

def Filterout(e, arg):
    #$(filter-out pattern...,text)
    return Filter(e, arg, True)

#TODO: the remaining functions

def Shell(e, arg): return ''

#################################################

class ClassENV:
    def __init__(self, obj):
        self.obj = obj
        self.__dict__['D'] = {}  # 'PATH':'', 'HOME':''

    def __getattr__(self, name):
        if name in self.D:
            return self.__dict__['D'][name]
        raise AttributeError(f"'DICT' has no attribute '{name}'")

    def __setattr__(self, name, value):
        if 'D' in self.__dict__ and name in self.__dict__['D']:
            self.__dict__['D'][name] = value

    def __getitem__(self, key):
        if key in self.__dict__['D']:
            return self.__dict__['D'][key]
        return ''

    def __setitem__(self, key, value):
        self.__dict__['D'][key] = value

    def __contains__(self, key):
        return key in self.__dict__['D']

    def delete(self, key):
        if key in self.D:
            del self.D[key]

    def dump(self, show = True):
        if show:
            print('[ENV]\n', str(self.__dict__['D']))
        return str( self.D )

    def export(self): # TODO
        # restore comma
        pass

    def call(self, fun):
        fun = fun.replace('˂', '(').replace('˃',')')
        try:
            fun = eval( fun ) # Function(self, ... )
        except Exception as E:
            ERROR('%s\n%s\n --->' % (E, fun) )
        return fun

    def subst(self, s):
        if '${' in s:
            pattern = re.compile(r"\$\{([a-zA-Z0-9_][a-zA-Z0-9_-]*)\}") # simple variable
            i = LIMIT
            m = re.search(pattern, s)
            while m:
                old = s
                key = m.group(1)
                if key in self.D:
                    s = s[ : m.start() ] + self.D[  m.group(1) ] + s[ m.end() : ]
                if s == old:
                    s = RESULT(s)
                    break
                m = re.search(pattern, s)
                if i == 0: ERROR('Recursive variable "%s" references itself (eventually).  Stop!' % key)
                i -= 1
        return self.execute(s)

    def execute(self, s):
        if '˂self' in s:
            pattern = re.compile(r'[A-Z][a-zA-Z]*˂[^˂˃]+˃') # get simple functions
            m = pattern.search(s)
            while m:
                s = s.replace( m.group(0), self.call( m.group(0) ) )
                m = pattern.search(s)
        return RESULT(s)

#################################################

class MK:
    def __init__(self, file, parent):
        self.dir = ''
        self.file = file
        self.parent = parent
        if parent:
            self.env = parent.env
        else: # main Makefile
            self.dir = dirname( os.path.abspath( file ) )
            os.chdir( self.dir )
            self.env = ClassENV( self )
        self.position = 0
        self.stack = []

    def transform(self, s):
        def cb1(m):
            return '${%s}' % m.group(1)
        s = s.replace('{', '(').replace('}', ')')
        s = re.sub( r"\$([a-zA-Z0-9])", cb1, s )                     # $x     --> ${x}
        s = re.sub( r"\$\(([a-zA-Z0-9_][a-zA-Z0-9_-]*)\)", cb1, s )  # $(KEY) --> ${KEY}

        pattern = r'\$\(([a-z][a-z-]+),([^\(\)]+)\)'
        m = re.search( pattern, s )
        while m:
            res = re.sub( pattern, "BadArgument˂self,None˃", s )
            if s == res:
                break
            s = res
            m = re.search(pattern, s)

        def cb3(m):
            fun = m.group(1).capitalize().replace('-','').strip()
            arg = m.group(3)
            return '%s˂self,"%s"˃' % ( fun, arg )
        pattern = r'\$\(([a-z][a-z-]+)(\s*)([^\(\)]+)\)'
        m = re.search( pattern, s )
        while m:
            res = re.sub( pattern, cb3, s )
            if s == res:
                break
            s = res
            m = re.search(pattern, s)

        return s

    def Read(self):
        #0. READ FILE
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                T0 = f.readlines()
                f.close()
                T0[-1] = T0[-1] + '\n'
        except Exception as e:
           ERROR('%s' % e)

        # EXPAND MULTILINES, REMOVE COMMENTS
        T1 = []
        current = ''
        ex = False
        for line in T0:
            line = line.replace('\r', '') # not need
            s = line.strip()
            if s.startswith('#') or s == '\n': # remove empty lines, '\n' is EOL
                continue

            if line.endswith('\\\n'):
                line = line[:-2]
                ex = True # expand begin

            if not line.endswith('\n'):
                current += line.lstrip() # expand
                continue

            if ex:
                current += line.lstrip()
                line = current.replace('\n', '')
                current = ''
                ex = False # expand end

            if not ex:
                line = line.replace('\n', '')
                i = line.find('#') # REMOVE MID COMMENT
                if i != -1:
                    line = line[ : i ]
                T1.append(line)

        #print(T1)

        # GET DEFINES, REMOVE EXPORT & OVERRIDE
        #print('[1]', T1)
        T2 = []
        a = ''
        start = False
        for line in T1:
            s = line.strip()
            if   s.startswith('export '):
                line = '#[export]   ' + line
                continue
            elif s.startswith('override '):
                line = '#[override]   ' + line
                continue
            elif s.startswith('define '):
                A = s.split(' ')
                a = A[1] + ' ' # VAR
                if len(A) > 2:
                    a += A[2] + ' ' # OP
                    if len(A) > 3:  # TEXT 1
                        a += ' '.join(A[3:]).strip() + ESC_ENTER
                else: a += '= '
                start = True
                continue
            elif s.startswith('endef'):
                line = a[ : -1 ] # remove last \n
                a = ''
                start = False
                pass
            elif start:
                a += line + ESC_ENTER # TEXT 2
                continue
            T2.append( line )

        # REMOVE RULES
        T3 = []
        for line in T2:
            s = line.strip()
            if s.startswith('$(info ') or s.startswith('$(info\t'):
                line = line.replace('$(info\t', '$(info ') #??
            elif s.startswith('$(dump'): pass
            elif s.startswith('$'):
                line = '#[$] ' + line
            else:
                state = 0
                cnt = 1
                a = ''
                if ':' in line:
                    for c in line:
                        if 0 == state:
                            if c == ':' or c == '=':
                                line = '#[r0] ' + line # error
                                break
                            state = 1
                            continue

                        elif 1 == state:
                            if c == ':': state = 2

                        elif 2 == state:
                            if c == '=': break
                            if c == ':':
                                cnt += 1
                                if cnt > 2:
                                    line = '#[r1] ' + line # :::
                                    break
                            else:
                                line = '#[r2] ' + line # ws
                                break

                        if c == '=': break

            T3.append( line )

        # TRANSFORM
        self.LINES = ['#[BEGIN]']
        for line in T3:
            self.LINES.append( self.transform( line ) )
        self.LINES.append('#[END]')

        #for s in self.LINES: print('[4]', s)
        #exit()
        pass

    def Set(self, unset = False):
        if unset: # Variable
            p = self.line.find('undefine')
            key = self.line[ p + 8 : ].strip()
            self.env.delete( key )
            return
        A = self.line.split('=', 1)
        if len( A ) == 2:
            key = A[0].strip()
            val = A[1].lstrip()
            val = RESULT(val)
            # NUTTX - DEPENDS !!! TODO
            op = '='
            if key.endswith('+') : op ='+'
            elif key.endswith(':') or key.endswith('::')   : op =':'
            elif key.endswith('?') and self.env[key] == '' : op ='?'
            key = key.replace('=', '').replace(':', '').replace('?', '')
            key = key.replace('+', '').replace('!', '').strip()
            if op == ':' or op == '::':
                self.env[ key ] = self.env.subst( val )
            elif op == '+':
                self.env[ key ] = self.env[ key ] + ' ' + val
            elif op == '?' and self.env[ key ] == '':
                self.env[ key ] = val
            else:
                self.env[ key ] = val

    def Expr(self):
        p = self.line.find('if')
        line = self.line[ p + 2 : ] # remove 'if'
        NOT = 'not' if 'n' == line[0] else ''
        if line.startswith('eq') or line.startswith('neq'):
            if line.startswith('eq'):
                line = line[ 2 : ].lstrip()
            else:
                line = line[ 3 : ].lstrip()
            if line.startswith('(') and line.endswith(')'):
                line = line [ 1 : -1 ]
            A = SPLIT(line, ',', 1)
            a = CLEAN( self.env.subst( A[0] ) )
            b = CLEAN( self.env.subst( A[1] ) )
            s = '%s( "%s" == "%s" )' % (NOT, a, b)
            res = eval(s)
            return res
        else:
            if line.startswith('def'):
                line = line[ 3 : ].lstrip()
            else:
                line = line[ 4 : ].lstrip()
            if self.line.startswith('(') and self.line.endswith(')'):
                line = line [1:-1]
            key = CLEAN( self.env.subst( line.strip() ) )
            res = eval( '%s(%s)' % (NOT, key in self.env) )
            return res

    def run_line(self):
        s = self.line.strip().replace(' ', '').replace('\n', ESC_ENTER)
        #print('[%.02d] %s' % (self.position+1,  self.line) )

        if  s.startswith('if'):
            res = self.Expr()
            self.stack.append(('if', self.position, res))
            if not res:
                self.skip_to(['elseif', 'else', 'endif'])

        elif s.startswith('elseif'):
            N,P,R = self.stack[-1] # peek ... Name, Pos, Res
            if R: # last Result
                self.skip_to(['endif'])
            else:
                self.stack.pop()
                result = self.Expr()
                self.stack.append( ('elseif', self.position, result) )
                if not result:
                    self.skip_to(['elseif', 'else', 'endif'])

        elif s.startswith('else'):
            N,P,R = self.stack[-1] # peek
            if R:
                self.skip_to(['endif'])
            else:
                N,P,R = self.stack.pop()
                self.stack.append(('else', self.position, False))

        elif s.startswith('endif'):
            N,P,R = self.stack.pop()

        elif s.startswith('include'):
            A = self.line.strip().split()
            file = CLEAN( self.env.subst(A[1]) )
            m = MK( file, self )
            m.Read()
            m.Run()

        elif re.match(r'^[A-Z][a-zA-Z]*˂', s):
            self.env.execute( self.line )

        elif s.startswith('undefine'):
            self.Set(True)

        else:
            self.Set()

    def Run(self):
        while self.position < len( self.LINES ):
            self.line = self.LINES[ self.position ]
            self.run_line()
            self.position += 1
        print('[EOF]', self.stack)

    def skip_to(self, targets):
        #print('\tSKIP_0', targets, self.stack)
        nest_level = 0
        while self.position < len( self.LINES ):
            self.position += 1 # NEXT
            s = self.LINES[ self.position ].replace(' ', '').strip()[:6]
            #print('\tSKIP-POS', self.position, s)
            if s.startswith('if'):
                #print('\tIF', self.stack, nest_level)
                nest_level += 1
                #print('\tIF', nest_level)
            elif s.startswith('endif'):
                #print('\tENDIF', self.stack, nest_level)
                if 0 == nest_level:
                    self.stack.pop()
                    #print('\tCURR-1', s, self.stack, self.position)
                    return
                nest_level -= 1
                #print('\tENDIF', nest_level)
            elif any( s == target for target in targets ) and nest_level == 0:
                self.position -= 1
                #print('\tCURR-2', s, self.stack, self.position)
                return

file = 'C:/Users/Georgi/Documents/PlatformIO/Projects/CMAKE/MK/TEST/or-and.mk'
m = MK( file, None )
m.Read()
m.Run()