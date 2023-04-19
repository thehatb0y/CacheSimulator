
class lru:
    def __init__(self):
        self.dict = {}

    def addToDict(self, item):
        self.plusOneDict()
        self.dict.update({item: 0})

    def plusOneDict(self):
        if len(self.dict) == 0:
            return 0
        for i in self.dict:
            self.dict[i] += 1

    def setItemToZero(self, item):
        self.dict[item] = 0

    def checkWhoCameFirst(self, lista_strings):
        valor_maximo = float('-inf') # inicializa com valor negativo muito baixo
        item_maximo = None
        for item in lista_strings:
            if item in self.dict and self.dict[item] > valor_maximo:
                valor_maximo = self.dict[item]
                item_maximo = item
        
        z = 0
        for i in lista_strings:
            if i == item_maximo:
                self.setItemToZero(item_maximo)
                return z
            z = z + 1
            
        return z



