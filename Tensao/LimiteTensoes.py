from abc import ABC, abstractmethod
from PSContBeam.carga_props.Concreto import Concreto

class LimTensao(ABC):
    
    @abstractmethod
    def lim_trac(self): pass

    @abstractmethod
    def lim_compr(self): pass

class LimElsF(LimTensao):

    def lim_trac(self, fctk_inf): 

        return 1.5*fctk_inf

    def lim_compr(self, fckj):

        return -.6*fckj    

class LimElsD(LimTensao):

    def lim_trac(self): 

        return 0

    def lim_compr(self, fckj): 

        return -.45*fckj

class LimEluAto(LimTensao):

    def lim_trac(self, fctmj): 

        return 1.2*fctmj
    
    def lim_compr(self, fckj): 

        return -.7* fckj

class LimFactory(LimTensao):

    types_t = ["els-f", "els-d", "elu-ato"]

    def __init__(self, concreto) -> None:

        self.c = Concreto(concreto)
    
    def lim_trac(self, name = "els-f"):

        if name not in self.types_t:
            raise TypeError("nome para o tipo de verificação nao existe!!!")
        if name == "els-f":
            return LimElsF().lim_trac(self.c.fctk_inf)
        if name == "els-d":
            return LimElsD().lim_trac()
        if name == "elu-ato":
            return LimEluAto().lim_trac(self.c.fctmj)
    
    def lim_compr(self, name = "els-f"):

        if name not in self.types_t:
            raise TypeError("nome para o tipo de verificação nao existe!!!")
        if name == "els-f":
            return LimElsF().lim_compr(self.c.fckj)
        if name == "els-d":
            return LimElsD().lim_compr(self.c.fckj)
        if name == "elu-ato":
            return LimEluAto().lim_compr(self.c.fckj)


