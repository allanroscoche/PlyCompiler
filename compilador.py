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
    'div'      :  'DIVIDE',
    'var'      :  'VAR',
    'input'    :  'INPUT',
    'output'   :  'OUTPUT'
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
import sys
import ply.lex as lex
lex.lex()

import tabela
rotulo = tabela.Rotulo()
tipo = tabela.Tipo()
tabela = tabela.TabelaExtendida()

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
                | program ID LPAREN lista_identificadores_programa RPAREN CMD bloco FIM'''
    print "\tPARA"


def p_statement_lista_identificadores_programa(t):
    '''lista_identificadores_programa : INPUT
                                      | OUTPUT
                                      | INPUT VIRG lista_identificadores_programa
                                      | OUTPUT VIRG lista_identificadores_programa'''


def p_statement_program(t):
    'program : PROGRAM'
    print "\tINPP"
    print "\tDSVS "+rotulo.nome()
    rotulo.add()

def p_statement_bloco(t):
    '''bloco : variaveis subrotinas comando_composto_inicial
             | variaveis comando_composto_inicial
             | subrotinas comando_composto_inicial
             | comando_composto_inicial '''
    print "\tDMEM "+str(tabela.getTam())

def p_statement_subrotinas(t):
    '''subrotinas : funcao
                  | procedimento
                  | funcao subrotinas
                  | procedimento subrotinas'''

def p_statement_funcao(t):
    '''funcao : function CMD DPONTOS tipo_retorno bloco CMD
              | function LPAREN lista_identificadores_sub RPAREN DPONTOS tipo_retorno CMD bloco CMD'''
    print "\tRTPR "+tabela.getNivel()


def p_statemente_function(t):
    'function : FUNCTION ID'
    print "\tDSVS "+rotulo.nome()
    rotulo.add()
    tabela.addFunc(t[2],rotulo.nome())
    print rotulo.nome()+ "\tNADA"
    rotulo.remove()
    tabela.sobeNivel()
    print "\tENPR "+tabela.getNivel()
    rotulo.add()
    tabela.resetParam()

def p_statement_tipo_retorno(t):
    '''tipo_retorno : INTEGER
                    | FLOAT '''
    tabela.funcao.setTipo(t[1])

def p_statement_procedimento(t):
    '''procedimento : procedure CMD bloco CMD
                    | procedure LPAREN lista_identificadores_sub RPAREN CMD bloco CMD'''
    print "\tRTPR "+tabela.getNivel()
    tabela.desceNivel()

def p_statement_procedure(t):
    'procedure : PROCEDURE ID'
    print "\tDSVS "+rotulo.nome()
    rotulo.add()
    tabela.addFunc(t[2],rotulo.nome())
    print rotulo.nome() + "\tNADA"
    rotulo.remove()
    tabela.sobeNivel()
    print "\tENPR "+tabela.getNivel()
    rotulo.add()
    tabela.resetParam()

def p_statement_variaveis(t):
    'variaveis : VAR declaracao_variaveis'
    print "\tAMEM "+str(tabela.getTam())

def p_statement_declaracao_variaveis(t):
    '''declaracao_variaveis : lista_identificadores_var DPONTOS tipo CMD
                            | lista_identificadores_var DPONTOS tipo CMD declaracao_variaveis'''

def p_statement_tipo(t):
    '''tipo : INTEGER
            | FLOAT   '''
    if t[1] == "integer":
        tabela.setType("integer")
    elif t[1]=="float" :
        tabela.setType("float")


def p_statement_lista_identificadores_sub(t):
    '''lista_identificadores_sub : parametro_formal
                                 | parametro_formal CMD lista_identificadores_sub'''
    #tabela.addParam(t[1],t[3])

def p_stamtement_parametro_formal(t):
    '''parametro_formal : VAR ID DPONTOS INTEGER
                        | ID DPONTOS INTEGER
                        | ID DPONTOS FLOAT
                        | VAR ID DPONTOS FLOAT '''
    if(t[1] == "var"):
        tabela.addParam(t[2],t[4],True)
    else:
        tabela.addParam(t[1],t[3])

def p_statement_lista_identificadores_var(t):
    '''lista_identificadores_var : ID
                                 | ID VIRG lista_identificadores_var'''
    tabela.addVar(t[1])

def p_statement_comando_composto_inicial(t):
    '''comando_composto_inicial : begin comando END
                                | begin comando mais_comandos END'''

def p_statement_comando_begin(t):
    'begin : BEGIN'
    rotulo.remove()
    print rotulo.nome()+"\tNADA"

def p_statement_comando_composto(t):
    '''comando_composto : BEGIN comando END
                        | BEGIN comando mais_comandos END'''

def p_statement_mais_comandos(t):
    '''mais_comandos : CMD comando
                     | CMD comando mais_comandos
                     | CMD '''

def p_statement_comando(t):
    '''comando : comando_composto
               | atribuicao
               | chamada_subprograma
               | comando_repetitivo
               | comando_condicional'''

def p_statement_chamada_procedimento(t):
    '''chamada_subprograma  : ID
                            | WRITE LPAREN lista_identificadores_write RPAREN
                            | READ LPAREN lista_identificadores_read RPAREN
                            | ID LPAREN lista_expressoes_subprograma RPAREN '''
    if t[1] != "write" and t[1] != "read":
        print "\tCHPR " + tabela.getVar(t[1]).getRotulo()
        tabela.resetParam()

def p_statement_lista_expressoes_subprograma(t):
    '''lista_expressoes_subprograma : ID
                                    | expression
                                    | ID VIRG lista_expressoes_subprograma
                                    | expression VIRG lista_expressoes_subprograma '''
    elem = tabela.useParam()
    if tabela.exists(t[1]):
        ident = tabela.getVar(t[1])
        if elem.referencia and not ident.referencia:
            print "\tCREN "+ident.getEnd()
        else:
            print "\tCRVL "+ident.getEnd()
    elif elem.referencia:
        print "ERRO: expressao encontrada na passagem por referencia ",elem
        raise SyntaxError

def p_statement_lista_identificadores_write(t):
    '''lista_identificadores_write : ID
                                   | ID VIRG lista_identificadores_write '''
    ident = tabela.getVar(t[1])
    print "\tCRVL " + ident.getEnd()
    print "\tIMPR"

def p_statement_lista_identificadores_read(t):
    '''lista_identificadores_read : ID
                                  | ID VIRG lista_identificadores_read'''
    print "\tLEIT"
    ident = tabela.getVar(t[1])
    print "\tARMZ " + ident.getEnd()

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
    if tabela.exists(t[1]):
        ident = tabela.getVar(t[1])
        if ident.eFuncao():
            ident = ident.retorno
            tabela.resetParam()
        if ident.referencia:
            print "\tARMI "+ident.getEnd()
        else:
            print "\tARMZ "+ident.getEnd()
        tipo.add(ident.getTipo())
        tipo.compara()
        tipo.reset()
    else:
        sys.stderr.write("ERRO: variavel nao definida: "+t[1]+"\n")
        raise SyntaxError

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
    tipo.compara()
    if   t[2] == '+'  : print "\tSOMA"
    elif t[2] == '-'  : print "\tSUBT"
    elif t[2] == '*'  : print "\tMULT"
    elif t[2] == "div": print "\tDIVI"
    elif t[2] == '>'  : print "\tCMMA"
    elif t[2] == '<'  : print "\tCMME"
    elif t[2] == '>=' : print "\tCMAG"
    elif t[2] == '<=' : print "\tCMEG"
    elif t[2] == '==' : print "\tCMDG"
    elif t[2] == '<>' : print "\tCMNE"

def p_expression_function_exp(t):
    'expression : ID LPAREN lista_expressoes_subprograma RPAREN'
    if tabela.exists(t[1]):
        ident = tabela.getVar(t[1])
        tabela.resetParam()
        print "\tCHPR " + ident.getRotulo()

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
    expression_tipo = "integer"

def p_expression_id(t):
    'expression : ID'
    if tabela.exists(t[1]) :
        ident = tabela.getVar(t[1])
        if ident.referencia:
            print "\tCRVI " + ident.getEnd()
        else:
            print "\tCRVL " + ident.getEnd()
        tipo.add(ident.getTipo())
    else:
        sys.stderr.write("ERRO: variavel nao definida:"+t[1]+"\n")
        raise SyntaxError

def p_error(t):
    print "Syntax error at '%s'" % t.value

import ply.yacc as yacc
yacc.yacc()

s = ""
while 1:
    try:
        s += raw_input() + " "
    except EOFError:
        break
#print s
yacc.parse(s)
#tabela.imprime()
