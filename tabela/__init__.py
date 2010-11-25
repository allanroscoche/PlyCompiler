class Rotulo:
    def __init__(self):
        self.cont = 0
        self.num = [0]
        #self.desvio = False
        #self.inicio = True

    def nome(self):
        if len(self.num) > 0:
            return "R"+str(self.num[len(self.num)-1])
        else:
            return "0"

    def add(self):
        self.cont += 1
        self.num.append(self.cont)

    def remove(self):
        self.num.pop()

class Variavel:
    def __init__(self,nome,end,tipo,nivel_lexico):
        self.nome = nome
        self.end = end
        self.tipo = tipo
        self.nivel_lexico = nivel_lexico

    def getEnd(self):
        endereco = str(self.nivel_lexico) + "," + str(self.end)
        return endereco

    def getTipo(self):
        return self.tipo

    def getNivel(self):
        return self.nivel_lexico

    def __str__(self):
        return "-->\t"+str(self.nome)+"\t"+str(self.end)+"\t"+str(self.tipo)

class Funcao:
    def __init__(self, nome, rotulo, tipo_retorno,nivel_lexico):
        self.rotulo = rotulo
        self.nome = nome
        self.tipo = tipo_retorno
        self.parametros = []
        self.endvar = -4
        self.nivel = nivel_lexico

    def setTipo(self,tipo):
        self.tipo = tipo

    def addParam(self,nome,tipo):
        parametro = Variavel(nome,self.endvar,tipo,self.nivel)
        self.parametros.append(parametro)
        self.nivel -= 1
        
    def getParam(self,nome):
        for i in self.parametros:
            if i.nome == nome:
                return i

    def getRotulo(self):
        return "R"+str(self.rotulo)

class Tipo:
    def __init__(self):
        self.tipoAtual = []

    def add(self,tipo):
        self.tipoAtual.append(tipo)

    def compara(self):
        if len(self.tipoAtual) > 0:
            atual = self.tipoAtual[0]
            for i in self.tipoAtual:
                if atual != i:
                    print "ERRO: "+i+" nao e compativel com "+atual
                    raise SyntaxError
    def reset(self):
        self.tipoAtual = []

    def imprime(self):
        for i in self.tipoAtual:
            print i


class Tabela:
    def __init__(self, nivel):
        self.num = 0
        self.tabela = {}
        self.nivel= nivel

    def addVar(self, nome, tipo, endereco=False):
        if not endereco:
            endereco = self.num
        variavel = Variavel(nome,endereco,tipo,self.nivel)
        self.tabela[nome] = variavel
        self.num += 1

    def addFunc(self, nome, rotulo, retorno):
        funcao = Funcao(nome, self.num, retorno, self.nivel)
        self.tabela[nome] = funcao
        self.funcao = nome
        self.num += 1
        return funcao

    def addParam(self, nome, tipo):
        print self.tabela[self.funcao].nome+" 2"
        self.tabela[self.funcao].addParam(nome,tipo)

    def getVar(self, nome):
        return self.tabela[nome]

    def exists(self, nome):
        if nome in self.tabela:
            return True
        else :
            return False

    def setType(self, tipo):
        for a, b in self.tabela.items():
            if b.tipo == "var":
                b.tipo = tipo

    def getTam(self):
        tam = 0
        for a, b in self.tabela.items():
            if b.__class__.__name__ == "Variavel":
                tam += 1
        return tam

    def imprime(self):
        for a, b in self.tabela.items():
            b.imprime()

class TabelaExtendida:
    def __init__(self):
        tabela = Tabela(0)
        self.pilha = [ tabela ]
        self.num_nivel = 0

    def getNivel(self):
        return str(self.num_nivel)

    def sobeNivel(self):
        self.num_nivel += 1
        tabela = Tabela(self.num_nivel)
        self.pilha.append(tabela)

    def desceNivel(self):
        if self.num_nivel >= 0:
            self.pilha.pop()
            self.num_nivel -= 1

    def addVar(self, nome):
        self.pilha[self.num_nivel].addVar(nome,"var")

    def addFunc(self, nome, rotulo):
        self.funcao = self.pilha[self.num_nivel].addFunc(nome, rotulo, "function")

    def addParam(self, nome, tipo):
        self.funcao.addParam(nome,tipo)
        param = self.funcao.getParam(nome)
        self.pilha[self.num_nivel].addVar(nome,tipo, param.end)

    def setType(self, tipo):
        self.pilha[self.num_nivel].setType(tipo)

    def exists(self, nome):
        existe = False
        for i in self.pilha:
            if i.exists(nome):
                existe = True
        return existe

    def getVar(self, nome):
        lista = range(self.num_nivel+1)
        lista.reverse()
        for i in lista:
            if self.pilha[i].exists(nome):
                return self.pilha[i].getVar(nome)
        raise SyntaxError

    def getTam(self):
        return self.pilha[self.num_nivel].getTam()
