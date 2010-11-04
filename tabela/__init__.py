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
