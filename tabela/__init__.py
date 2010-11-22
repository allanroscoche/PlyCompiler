class Rotulo:
    def __init__(self):
        self.cont = 0
        self.num = [0]
        self.desvio = False
        self.inicio = True

    def nome(self):
        #print self.num
        return "R"+str(self.num[len(self.num)-1])

    def add(self):
        self.cont += 1
        self.num.append(self.cont)

    def remove(self):
        self.num.pop()

class VarGlobais:
    def __init__(self):
        self.cont = 0
        self.alocado = 0

    def add(self):
        self.cont += 1

    def imprime(self):
        tmp = str(self.cont)
        self.alocado = self.cont
        self.cont = 0
        return tmp

    def total(self):
        tmp = str(self.alocado)
        self.alocado = 0
        return tmp

class Variavel:
    def __init__(self,nome,end,tipo):
        self.nome = nome
        self.end = end
        self.tipo = tipo

    def getEnd(self):
        return self.end

    def getTipo(self):
        return self.tipo

    def imprime(self):
        print str(self.nome)+"\t"+str(self.end)+"\t"+str(self.tipo)


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
        self.nivel_lex = nivel

    def add(self, nome, tipo):
        variavel = Variavel(nome,self.num,tipo)
        self.tabela[nome] = variavel
        self.num += 1

    def getVar(self, nome):
        return self.tabela[nome]

    def exists(self, nome):
        if nome in self.tabela:
            return True
        else :
            return False

    def setType(self, tipo):
        for a, b in self.tabela.items():
            if b.tipo == "undefined":
                b.tipo = tipo

    def imprime(self):
        for a, b in self.tabela.items():
            b.imprime()

class TabelaExtendida:
    def __init__(self):
        tabela = Tabela(0)
        self.pilha = [ tabela ]
        self.num_nivel = 0

    def sobeNivel(self):
        self.niveis += 1
        tabela = Tabela(self.num_nivel)
        self.pilha.append(tabela)

    def desceNivel(self):
        if self.num_nivel >= 0:
            self.pilha.remove(self.num_nivel)
            self.num_nivel -= 1

    def add(self, nome):
        self.pilha[self.num_nivel].add(nome,"undefined")

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

