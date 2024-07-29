from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from PSContBeam.Tensao.LimiteTensoes import LimFactory

class PlotResultados(ABC):

    @abstractmethod
    def plot(): pass
    @abstractmethod
    def show(): pass

class PlotTensao(PlotResultados):

    def __init__(self,x,tensao, lim: LimFactory, name, **kwargs):


        self.x = x
        self.sup = tensao.sup()
        self.inf = tensao.inf()
        self.lim_inf = np.array(lim.lim_compr(name = name))
        self.lim_sup = np.array(lim.lim_trac(name = name))
        self.name = name
        #adicionando resultados para comparação
        self.verific = bool(kwargs)
        if self.verific:
            self.xv = self.x
            self.yvi = kwargs["inf"]
            self.yvs = kwargs["sup"]
#print(lim_inf, lim_sup)

        plt.rc('font', family='Times New Roman', size= 12)
        plt.style.use('bmh')

        fig , (ax1, ax2) = plt.subplots(2, 1)
        fig.subplots_adjust(hspace=0.426, top= .92, bottom=.09)
        self.ax1 = ax1
        self.ax2 = ax2

    def plot(self):
#adicionando os limites de tração e compressão
        self.ax1.hlines(self.lim_sup, self.x[0], self.x[-1], colors= "r", linestyles= "--")
        self.ax1.hlines(self.lim_inf, self.x[0], self.x[-1], colors= "r", linestyles= "--")
        self.ax2.hlines(self.lim_sup, self.x[0], self.x[-1], colors= "r", linestyles= "--")
        self.ax2.hlines(self.lim_inf, self.x[0], self.x[-1], colors= "r", linestyles= "--")
        nt, nc = self.names_lim(self.name)
        self.ax1.annotate(nt, (self.x[-1], self.lim_sup), color= "r")
        self.ax1.annotate(nc, (self.x[-1], self.lim_inf), color= "r")
        self.ax2.annotate(nt, (self.x[-1], self.lim_sup), color= "r")
        self.ax2.annotate(nc, (self.x[-1], self.lim_inf), color= "r")

#adicionando labels
        self.ax1.set_title(f"{self.name.upper()} Fibra Superior")
        self.ax1.set_xlabel("Comprimento (m)")
        self.ax1.set_ylabel("\u03C3 (MPa)")
        self.ax2.set_title(f"{self.name.upper()} Fibra Inferior")
        self.ax2.set_xlabel("Comprimento (m)")
        self.ax2.set_ylabel("\u03C3 (MPa)")

        #plotando graficos
        self.ax1.plot(self.x, self.sup , "b", label = "PsContBeam")
        self.ax2.plot(self.x, self.inf , "b", label = "PsContBeam")
        if self.verific:
            self.ax1.plot(self.x, self.yvs, "k.", label = "TQS VPRO") #"TQS VPRO"
            self.ax2.plot(self.x, self.yvi, "k.", label = "TQS VPRO")
        self.ax1.legend(loc = 'lower right')
        self.ax2.legend(loc = 'lower right')
        self.ax1.grid(':')
        self.ax2.grid(":")

        #limites horizontais
        lim = 3.5
        self.ax1.set_xlim(self.x[0], self.x[-1])
        self.ax1.set_ylim(np.min(self.sup)-lim ,np.max(self.sup)+lim)
        self.ax2.set_xlim(self.x[0], self.x[-1])
        self.ax2.set_ylim(np.min(self.inf)-lim,np.max(self.inf)+lim)
    
    def show(self):
        plt.show()


    def names_lim(self, name = 'els-f'):

        if name == 'els-f':
            sup = "1.5fctk,inf"
            inf = "0.6.fckj"
            return sup, inf
        if name == 'els-d':
            sup = "0.0"
            inf = "0.45.fckj"
            return sup, inf
        if name == 'elu-ato':
            sup = "1.2fctmj"
            inf = "0.7.fckj"
            return sup, inf




class PlotForce(PlotResultados):

    def __init__(self,x , f0, finf):
        self.x = x
        self.f0 = f0
        self.finf = finf

        plt.rc('font', family='Times New Roman', size= 12)
        plt.style.use('bmh')
        self.pf = plt

    def plot(self):
        self.pf.plot(self.x, self.finf, "b", label = "t = \u221E")
        self.pf.plot(self.x, self.f0, "k.", label = "t = O")
        self.pf.grid(linestyle= ":")
        self.pf.title("Força de Protensão")
        self.pf.xlabel("Comprimento (m)")
        self.pf.ylabel("f (tf)")
        self.pf.xlim(self.x[0], self.x[-1])
        self.pf.legend(loc = 'upper right')

    def show(self):
        self.pf.show()
        

class PlotMomentoHiperestatico(PlotResultados):
    
    def __init__(self,x, m0, m):
        self.x = x
        self.m0 = m0
        self.m = m
        plt.rc('font', family='Times New Roman', size= 12)
        plt.style.use('bmh')
        self.mh = plt

    def plot(self):

        self.mh.plot(self.x,self.m, "b", label = "t = \u221E")
        self.mh.plot(self.x,self.m0, "k.", label = "t = O")
        self.mh.grid(linestyle= ":")
        self.mh.title("Momento Hiperestático de Protensão")
        self.mh.xlabel("Comprimento (m)")
        self.mh.ylabel("Momento (tf*m)")
        self.mh.xlim(self.x[0], self.x[-1])
        self.mh.legend(loc = 'lower right')

    def show(self):
        self.mh.show()


