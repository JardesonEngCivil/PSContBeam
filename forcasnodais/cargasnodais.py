from PSContBeam.protensao.force import ForceFactory
from PSContBeam.protensao.functracado import TracadoFactory
from PSContBeam.protensao.functracado import Retilineo
from PSContBeam.protensao.functracado import ParabolaSimples
from PSContBeam.protensao.functracado import ParabolaInflexao
import numpy as np

class MomentosNodais(dict):
    def __init__(self, tracado,force, cg, size = 1):
        self.cg = cg
        self.tracado = TracadoFactory(tracado, cg)
        self.force   = ForceFactory(force).force()
        self.size    = size
        self._params = []
        self["m"]    = []
        self["m0"]   = []
        self["x"]    = []

        self.calc_momentos()

    def discretize(self, trecho):
        start = trecho.x0
        end   = trecho.xf
        if self.size > end:
            raise ValueError(f"{self.size} é maior que o trecho")
        
        num = int(round((end - start)/self.size, 0) + 1)
        list_tmp = list(np.linspace(start= start, stop= end, num =  num ))
        list_tmp = [round(i,3) for i in list_tmp]
        list_tmp = [[list_tmp[i], list_tmp[i+1]] for i in range(len(list_tmp) - 1)]
        return list_tmp
    
    def params_ret(self, trecho):

        for i in self.discretize(trecho):  
            x = (i[1] + i[0]) / 2
            l = i[1] - i[0]
            area = Gauss()._area(trecho, i[0], i[1])
            self._params.append([x, l, area])
            self["x"].append(i[0])

    def params_parabola_simples(self, trecho):

        for i in self.discretize(trecho):
            x = (i[1] + i[0]) / 2
            l = i[1] - i[0]
            area = Gauss()._area(trecho, i[0], i[1])
            self._params.append([x, l, area])
            self["x"].append(i[0])
        
    def params_parabola_inflexao(self, trecho):
        
        for i in self.discretize(trecho):
            #print(i)
            x = (i[1] + i[0]) / 2
            l = i[1] - i[0]
            xf = i[1] - trecho.x0
            x0 = i[0] - trecho.x0
            xi = trecho.xi
            area = Gauss()._area(trecho, i[0], i[1])
            self._params.append([x, l, area])
            #print(x0, xi, xf)
            #if xf > xi and x0  < xi:
            # if i[1] > xi and i[0]  < xi:
            # #     #print("ol")
            # #     #print(i[0], xi, i[1])
            #     limite1 = [i[0], xi]
            #     limite2 = [xi, i[1]]
            #     area = Gauss()._area(trecho, limite1[0], limite1[1])
            #     area += Gauss()._area(trecho, limite2[0], limite2[1])
            #     area = l*trecho.cg - area
            #     self._params.append([x, l, area])
            # else:
            #     area = Gauss()._area(trecho, i[0], i[1])
            #     area = l*trecho.cg - area
            #     self._params.append([x, l, area])

            self["x"].append(i[0])

    def params_factory(self):

        for trecho in self.tracado:
            if isinstance(trecho, Retilineo):
                self.params_ret(trecho)
            if isinstance(trecho, ParabolaSimples):
                self.params_parabola_simples(trecho)
            if isinstance(trecho, ParabolaInflexao):
                self.params_parabola_inflexao(trecho)

        self["x"].append(float(trecho.xf))

    def calc_momentos(self):
        self.params_factory()
        for i in self._params:
            x    = i[0]
            l    = i[1]
            area = i[2]
            m = self.force.finf(x)*area/l
            m0 = self.force.f0(x)*area/l
            # self["m"].append(m)
            # self["m0"].append(m0)
            if bool(self["m"]) is False:
                self["m0"].append(m0)
                self["m0"].append(-m0)
                self["m"].append(m)
                self["m"].append(-m)
                
            else:
                self["m0"][-1] += m0
                self["m0"].append(-m0)
                self["m"][-1] += m
                self["m"].append(-m)

class Gauss:

    def __init__(self) -> None:
        self._x = np.array([-np.sqrt(1/3), np.sqrt(1/3)])
        self._w = np.array([1, 1])
     
    def _eps(self,a, b):

        self.eps = self._x*(b - a)/2 + (b + a)/2
        return self.eps

    def _area(self, func, a, b):
        
        area = 0
        for i in self._eps(a, b):
            area += 1*func.t(i)
        area *= (b - a)/2
        return area

if __name__ == "__main__":
    t = [["parabola",  [[0.0, 0.25], [4, 0.08]], 0.25],
        ["parabola",  [[4, 0.08], [8, 0.25]], 0.25],
        ["parabola",  [[8, 0.25], [12, 0.08]], 0.25],
        ["parabola",  [[12.0, 0.08],[16.0, 0.25]], 0.25]]
    f = {   
        "type" : "discreto",
            "x" : [0,1,2,3,4,5,6,7,8,9,10, 11,12, 13,14, 15,16],

                "f0" :[14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
                , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9],

            "finf": [14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
            , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9]
            

        }

    m = MomentosNodais(t, f)
    print(m)
