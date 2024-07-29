
class Combinacao:

    def __init__(self, carregamento : dict):

        self.carregamento = carregamento
        self.Psi1 = {"residencial": .4, "comercial": .6
            , "Biblioteca, arquivos, oficinas e garagens": .7}
        
        self.Psi2 = {"residencial": .3, "comercial": .4
            , "Biblioteca, arquivos, oficinas e garagens": .6}

    @property
    def CF(self):

        cf = self.carregamento["permanente"] + self.carregamento["peso_proprio"] + \
        self.carregamento["acidental"]*self.Psi1[self.carregamento["tipo"]]#cq = p + pp + q*self.Psi1[tipo]

        return cf

    @property
    def CQP(self):
        
        cqp = self.carregamento["permanente"] + self.carregamento["peso_proprio"] + \
        self.carregamento["acidental"]*self.Psi2[self.carregamento["tipo"]]

        return cqp
    
    @property
    def ATO(self):
        ato =  self.carregamento["peso_proprio"]
        
        return ato