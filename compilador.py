#! /usr/bin/env python

reserved = {
    'if'       :  'IF',
    'then'     :  'THEN',
    'else'     :  'ELSE',
    'program'  :  'PROGRAM',
    'begin'    :  'BEGIN',
    'end'      :  'END',
    'procedure':  'PROCEDURE',
    'while'    :  'WHILE',
    'do'       :  'DO'
    }

tokens = [
    'NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','ATTRIB',
    'LESS', 'LESS_EQ', 'MORE', 'MORE_EQ','EQUAL','DIFF',
    'LPAREN','RPAREN','ID'
    ]+list(reserved.values())

# Tokens

t_MORE    = r'>'
t_LESS    = r'<'
t_MORE_EQ = r'<='
t_LESS_EQ = r'>='
t_EQUAL   = r'=='
t_DIFF    = r'!='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_ATTRIB  = r':='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left','LESS','MORE','LESS_EQ','MORE_EQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_if(t):
    'statement : IF expression_if THEN statement'
    print "NADA"

def p_statement_while_do(t):
    'statement : while expression_while DO statement'
    print "NADA"

def p_statement_while(t):
    'while : WHILE'
    print "NADA"

def p_statement_assign(t):
    'statement : ID ATTRIB expression'
    print "ARMZ "+str(t[1])
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'

def p_statement_expr_if(t):
    'expression_if : expression'
    print "DSVF"

def p_statement_expr_while(t):
    'expression_while : expression'
    print "DSVF"

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LESS expression
                  | expression MORE expression
                  | expression LESS_EQ expression
                  | expression MORE_EQ expression
                  | expression EQUAL expression
                  '''
    if t[2] == '+'   : print "SOMA"
    elif t[2] == '-' : print "SUBT"
    elif t[2] == '*' : print "MULT"
    elif t[2] == '/' : print "DIVI"
    elif t[2] == '>' : print "CM01"
    elif t[2] == '<' : print "CM02"
    elif t[2] == '>=': print "CM03"
    elif t[2] == '<=': print "CM04"
    elif t[2] == '==': print "CMEG"
    elif t[2] == '!=': print "CMNE"

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    print "CRCT "+ str(t[1])
    t[0] = t[1]

def p_expression_id(t):
    'expression : ID'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print "Undefined name '%s'" % t[1]
        t[0] = 0

def p_error(t):
    print "Syntax error at '%s'" % t.value

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('entrada > ')
    except EOFError:
        break
    yacc.parse(s)
