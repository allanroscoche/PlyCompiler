class Rotulo:
    def __init__(self):
        self.cont = 0
        self.num = [0]

    def nome(self):
        #print self.num
        return "R"+str(self.num[len(self.num)-1])

    def add(self):
        self.cont += 1
        self.num.append(self.cont)

    def remove(self):
        self.num.remove(self.cont)

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

    def getEndereco(self):
        return self.end

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
    def __init__(self):
        self.num = 0
        self.tabela = {}

    def add(self, nome, tipo):
        variavel = Variavel(nome,self.num,tipo)
        self.tabela[nome] = variavel
        self.num += 1

    def getEnd(self, nome):
        return self.tabela[nome].getEndereco()

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
