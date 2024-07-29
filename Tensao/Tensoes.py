from abc import ABC, abstractmethod
import numpy as np
#minhas exportações
from PSContBeam.momentos.momentos import MomentoHiperestatico, MomentoExterno, particionamento
from PSContBeam.momentos.momentos import MomentoExterno
from PSContBeam.momentos.exentricidade import Exentricidade
from PSContBeam.protensao.force import ForceFactory
from PSContBeam.Plotagem.ploter import PlotTensao, PlotForce, PlotMomentoHiperestatico
from PSContBeam.Tensao.LimiteTensoes import LimFactory


class TensaoNormal(ABC):

    @abstractmethod
    def sup(): pass

    @abstractmethod
    def inf(): pass

    
class ELS_F(TensaoNormal):
    def __init__(self,**kwargs):

        self.f      = -kwargs["f"]
        self.e      = kwargs["e"]
        self.mhiper = kwargs["m"]
        self.mext   = kwargs["ms"]
        self.A      = kwargs["A"]
        self.wi     = kwargs["wi"]
        self.ws     = kwargs["ws"]


    def inf(self):
    
        f_A = self.f/self.A
        ms_wi = self.mext/self.wi
        iso_hiper = (self.f*self.e + self.mhiper)/self.wi
        t = f_A + ms_wi + iso_hiper
        return t/100
    
    def sup(self):
        
        f_A = self.f/self.A
        ms_wi = self.mext/self.ws
        iso_hiper = (self.f*self.e + self.mhiper)/self.ws
        t = f_A + ms_wi + iso_hiper
        return t/100
        

class ELS_D(TensaoNormal):
    def __init__(self, **kwargs):
        self.f      = -kwargs["f"]
        self.e      = kwargs["e"]
        self.mhiper = kwargs["m"]
        self.mext   = kwargs["ms"]
        self.A      = kwargs["A"]
        self.wi     = kwargs["wi"]
        self.ws     = kwargs["ws"]

    def inf(self):
        
        f_A = self.f/self.A
        ms_wi = self.mext/self.wi
        iso_hiper = (self.f*self.e + self.mhiper)/self.wi
        t = f_A + ms_wi + iso_hiper
        return t/100
    
    def sup(self):
        
        f_A = self.f/self.A
        ms_wi = self.mext/self.ws
        iso_hiper = (self.f*self.e + self.mhiper)/self.ws
        t = f_A + ms_wi + iso_hiper
        return t/100
 
    
class ELU_ATO(TensaoNormal):
    
    def __init__(self,**kwargs):
        self.f      = -1.1*kwargs["f"]
        self.e      = kwargs["e"]
        self.mhiper = kwargs["m"]
        self.mext   = kwargs["ms"]
        self.A      = kwargs["A"]
        self.wi     = kwargs["wi"]
        self.ws     = kwargs["ws"]

        # for i in range(len(self.mhiper)):
        #     if self.mext[i] < 0:
        #         self.mhiper[i] = self.mhiper[i]*0.95
        #     else:
        #         self.mhiper[i] = self.mhiper[i]*1.1

    def inf(self):
        f_A = self.f/self.A
        ms_wi = self.mext/self.wi
        iso_hiper = (self.f*self.e + 1.1*self.mhiper)/self.wi
        t = f_A + ms_wi + iso_hiper
        return t/100
    
    def sup(self):
        f_A = self.f/self.A
        ms_wi = self.mext/self.ws
        iso_hiper = (self.f*self.e + 1.1*self.mhiper)/self.ws
        t = f_A + ms_wi + iso_hiper
        return t/100

class Tensao():
    
    def __init__(self, dados_glob, size = 1, not_pp = False, part = 1) -> None:
        self.dados_glob = dados_glob
        self.size       = size
        self.not_pp     = not_pp
        self.part       = part

        self.tracado      = self.dados_glob["tracado"]
        self.estrutura    = self.dados_glob["estrutura"]
        self.force        = self.dados_glob["forca_protensao"]
        self.carregamento = self.dados_glob["carregamento"]
        self.props        = self.dados_glob["props"]
        self.concreto     = self.dados_glob["concreto"]

    @property
    def e(self):
        return np.round(Exentricidade(self.tracado, self.cg, self.part),4)
    
    @property
    def m_hiper(self):
        m_hiper = MomentoHiperestatico(self.tracado, self.force,self.estrutura,
                                        self.props["cg"], self.size, self.part)
        return {"m": np.array(m_hiper.m), "m0": np.array(m_hiper.m0)}
    
    @property
    def m_ext(self):
        m_ext = MomentoExterno(self.estrutura,self.carregamento, not_pp= self.not_pp, part= self.part)
        return {"CF": np.array(m_ext.CF), "CQP": np.array(m_ext.CQP), "ATO": np.array(m_ext.ATO)}
    
    @property
    def finf(self):
        f = ForceFactory(self.force).force()
        f = np.array([f.finf(i) for i in self.x])
        return f
    
    @property
    def f0(self):
        f0 = ForceFactory(self.force).force()
        f0 = np.array([f0.f0(i) for i in self.x])
        return f0
    
    @property 
    def x(self):
        xi = list(self.estrutura["nos"].values())[0]
        xf = list(self.estrutura["nos"].values())[-1]
        return particionamento(xi, xf, self.part)
    
    @property
    def A(self): 
        return self.props["A"]
    
    @property
    def E(self): 
        return self.props["E"]
    
    @property
    def I(self): 
        return self.props["I"]
    
    @property
    def cg (self):
        return self.props["cg"]
    
    @property
    def wi(self): 
        return self.I/self.cg
    
    @property
    def ws(self): 
        return -self.wi
    
    
    def els_f(self)-> TensaoNormal:
        return ELS_F(f = self.finf, e= self.e, m= self.m_hiper["m"],
                     ms= self.m_ext["CF"], A = self.A,
                     wi= self.wi, ws= self.ws)
    
    def els_d(self)-> TensaoNormal:
        return ELS_D(f = self.finf, e= self.e, m= self.m_hiper["m"],
                     ms= self.m_ext["CQP"], A = self.A,
                     wi= self.wi, ws= self.ws)

    def elu_ato(self)-> TensaoNormal:
        return ELU_ATO(f = self.f0, e= self.e, m= self.m_hiper["m0"],
                     ms= self.m_ext["ATO"], A = self.A,
                     wi= self.wi, ws= self.ws)
    
    
    def plot_els_f(self) -> None:
        lim = LimFactory(self.concreto)
        plot = PlotTensao(self.x,self.els_f(),lim, 'els-f')
        plot.plot()
        plot.show()

    def plot_els_f(self, **kwargs) -> None:
        lim = LimFactory(self.concreto)
        plot = PlotTensao(self.x,self.els_f(),lim, 'els-f', **kwargs)
        plot.plot()
        plot.show()
    
    def plot_els_d(self, **kwargs) -> None:
        lim = LimFactory(self.concreto)
        plot = PlotTensao(self.x,self.els_d(),lim, 'els-d', **kwargs)
        plot.plot()
        plot.show()

    def plot_elu_ato(self, **kwargs) -> None:
        lim = LimFactory(self.concreto)
        plot = PlotTensao(self.x,self.elu_ato(),lim, 'elu-ato', **kwargs)
        plot.plot()
        plot.show()  

    def plot_f(self):
        plot = PlotForce(self.x,self.f0, self.finf) 
        plot.plot()
        plot.show()
    
    def plot_momento_hiperestatico(self):
        plot = PlotMomentoHiperestatico(self.x,-self.m_hiper["m0"], -self.m_hiper["m"])
        plot.plot()
        plot.show()

    
    
    
if __name__ == "__main__":
    ...
