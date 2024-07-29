import numpy as np

class Concreto:
    def __init__(self, concreto):
        

        self.fck  = concreto["fck"]
        self.t    = concreto["tempo"] 
        self.tipo = concreto["tipo_cimento"]
        self.s    = {"CP I": .25, "CP II": .25,
            "CP III": .38, "CP IV": .38,
            "CP V-ARI": .2}

    @property  
    def b1(self):

        b1 = np.exp(self.s[self.tipo.upper()]*(1-np.sqrt(28/self.t)))
        return b1
    
    @property
    def fckj(self):

        fckj = self.b1*self.fck
        return fckj
    
    @property
    def fctmj(self):
        fctmj= .3*(self.fckj)**(2/3)
        return fctmj

    @property
    def fctk_inf(self):

        fctk_inf = .7*.3*(self.fck)**(2/3)
        return fctk_inf 
    