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
    'do'       :  'DO',
    'var'      :  'VAR',
    'integer'  :  'INTEGER',
    'float'    :  'FLOAT',
    'write'    :  'WRITE',
    'read'     :  'READ',
    'function' :  'FUNCTION',
    'procedure':  'PROCEDURE',
    'div'      :  'DIVIDE'
    }

tokens = [
    'NUMBER', 'CMD', 'FIM', 'DPONTOS', 'VIRG',
    'PLUS','MINUS','TIMES','ATTRIB',
    'LESS', 'LESS_EQ', 'MORE', 'MORE_EQ','EQUAL','DIFF',
    'LPAREN','RPAREN','ID'
    ]+list(reserved.values())

# Tokens

t_FIM     = r'.'
t_CMD     = r'\;'
t_MORE    = r'>'
t_LESS    = r'<'
t_MORE_EQ = r'<='
t_LESS_EQ = r'>='
t_EQUAL   = r'='
t_DIFF    = r'!='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
t_ATTRIB  = r'\:='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_DPONTOS = r'\:'
t_VIRG    = r','

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

contador=0

def t_newline(t):
    r'\n+'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

import tabela
rotulo = tabela.Rotulo()

# Parsing rules

precedence = (
    ('left','LESS','MORE','LESS_EQ','MORE_EQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_init(t):
    '''programa : program ID CMD bloco FIM
                | program ID LPAREN lista_identificadores RPAREN CMD bloco FIM'''
    print "\tPARA"

def p_statement_program(t):
    'program : PROGRAM'
    print "\tINIT"

def p_statement_bloco(t):
    '''bloco : variaveis subrotinas comando_composto
             | variaveis comando_composto
             | subrotinas comando_composto
             | comando_composto '''

def p_statement_subrotinas(t):
    '''subrotinas : funcao
                  | procedimento
                  | funcao subrotinas
                  | procedimento subrotinas'''

def p_statement_funcao(t):
    'funcao : FUNCTION ID CMD comando_composto'
    print "funcao"

def p_statement_procedimento(t):
    'procedimento : PROCEDURE ID CMD bloco CMD'
    print "procedimento"

def p_statement_variaveis(t):
    'variaveis : VAR declaracao_variaveis'
    print "\tAMEM"

def p_statement_declaracao_variaveis(t):
    '''declaracao_variaveis : lista_identificadores DPONTOS tipo CMD
                            | lista_identificadores DPONTOS tipo CMD declaracao_variaveis'''

def p_statement_tipo(t):
    '''tipo : INTEGER
            | FLOAT '''

def p_statement_lista_identificadores(t):
    '''lista_identificadores : ID
                             | ID VIRG lista_identificadores'''

def p_statement_comando_composto(t):
    '''comando_composto : BEGIN comando END
                        | BEGIN comando mais_comandos END'''

def p_statement_mais_comandos(t):
    '''mais_comandos : CMD comando
                     | CMD comando mais_comandos '''

def p_statement_comando(t):
    '''comando : comando_composto
               | atribuicao
               | chamada_procedimento
               | comando_repetitivo
               | comando_condicional'''

def p_statement_chamada_procedimento(t):
    '''chamada_procedimento : ID
                            | write LPAREN lista_identificadores RPAREN
                            | read LPAREN lista_identificadores RPAREN
                            | ID LPAREN lista_identificadores RPAREN '''

def p_statement_write(t):
    'write : WRITE'
    print "\twrite"

def p_statement_read(t):
    'read : READ'
    print "\tLEIT"

def p_statement_if(t):
    '''comando_condicional : IF expression_if THEN comando
                           | IF expression_if THEN comando ELSE comando'''
    print rotulo.nome() + "\tNADA"
    rotulo.remove()

def p_statement_while_do(t):
    'comando_repetitivo : while expression_while DO comando'
    print rotulo.nome() + "\tNADA"
    rotulo.remove()

def p_statement_while(t):
    'while : WHILE'
    print rotulo.nome() + "\tNADA"

def p_statement_atribuicao(t):
    'atribuicao : ID ATTRIB expression'
    print "\tARMZ "+str(t[1])
    names[t[1]] = t[3]

def p_statement_expr_if(t):
    'expression_if : expression'
    rotulo.add()
    print "\tDSVF " + rotulo.nome()

def p_statement_expr_while(t):
    'expression_while : expression'
    rotulo.add()
    print "\tDSVF " + rotulo.nome()

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
    if   t[2] == '+'  : print "\tSOMA"
    elif t[2] == '-'  : print "\tSUBT"
    elif t[2] == '*'  : print "\tMULT"
    elif t[2] == "div": print "\tDIVI"
    elif t[2] == '>'  : print "\tCM01"
    elif t[2] == '<'  : print "\tCM02"
    elif t[2] == '>=' : print "\tCM03"
    elif t[2] == '<=' : print "\tCM04"
    elif t[2] == '==' : print "\tCMEG"
    elif t[2] == '!=' : print "\tCMNE"

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    print "\tCRCT "+ str(t[1])
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

import sys
import ply.yacc as yacc
yacc.yacc()

s = ""
while 1:
    try:
        s += raw_input() + " "
    except EOFError:
        break
print s
yacc.parse(s)
