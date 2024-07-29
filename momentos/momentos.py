
from PSContBeam.momentos.viga import ElementosBarra, ApoiosBarra
from PSContBeam.momentos.reaction import  Reacao
from PSContBeam.carga_props.Combinacao import Combinacao
from abc import ABC, abstractmethod
from anastruct import SystemElements
import numpy as np
from copy import deepcopy


class Momento(ABC):

    @abstractmethod
    def inserir_elementos():pass
    
    @abstractmethod
    def inserir_apoios():pass

    @abstractmethod
    def _add_momentos(): pass

class MomentoHiperestatico(Momento):

    def __init__(self, tracado,force, estrutura,cg, size = .5, part= 1):

        self.r = Reacao(tracado,force, estrutura,cg, size = size)
        self.v = SystemElements(mesh = 10)
        self.estrutura = estrutura
        self.part = part
        self.nos, self.elementos, self.apoios = self.estrutura
        self._dict = {}
        self._add_momentos()

    def set_loc(self):
        xi = list(self.estrutura[self.nos].values())[0]
        xf = list(self.estrutura[self.nos].values())[-1]
        return particionamento(xi,xf, self.part)
    
    def inserir_elementos(self):
        self._dict["x"] = self.set_loc()
        ElementosBarra(self.estrutura).add_elementos(self.v, self._dict["x"])
    
    def inserir_apoios(self):
        tmp = deepcopy(self.estrutura[self.apoios])
        for i in list(self.estrutura[self.apoios])[1:-1]:
            tmp.pop(i)
        
        ins_apoios = ApoiosBarra(self.estrutura)
        ins_apoios.add_apoio(self.v, ins_apoios.nos_apoios_iso(self.v, tmp))

    def inserir_f_nodias(self,typ):
        for f in self.r[typ]:
            no = self.v.find_node_id([f[0], 0])
            self.v.point_load(node_id= no, Fy = -f[1])
    
    def solve(self):
        self.v.solve()
    
    def setter_m(self):
        typ = ["m", "m0"]
        for i in typ:
            self.inserir_f_nodias(i)
            self.solve()
            self._dict[i] = self.get_momentos()
            self.v.remove_loads(True)

    def get_momentos(self):
        tmp_m = self.v.get_element_results(element_id=0, verbose= True)
        Momento = [-i["M"][0] for i in tmp_m]
        Momento.append(-tmp_m[-1]["M"][-1])
        return Momento
    
    def _add_momentos(self):
        self.inserir_elementos()
        self.inserir_apoios()
        self.setter_m()


    @property
    def m(self): return self._dict["m"]

    @property
    def m0(self): return self._dict["m0"]

    @property
    def x(self): return self._dict["x"]

class MomentoExterno(Momento):
    
    def __init__(self, estrutura, carregamento, not_pp = False, part = 1):
        self.estrutura = estrutura
        self.nos, self.elementos, self.apoios = self.estrutura
        self.comb = Combinacao(carregamento)
        self.not_pp = not_pp
        self.part = part
        self.v = SystemElements(mesh = 10)
        self._dict = dict()
        self._add_momentos()
    
    def set_loc(self):
        xi = list(self.estrutura[self.nos].values())[0]
        xf = list(self.estrutura[self.nos].values())[-1]
        return particionamento(xi,xf, self.part)
    
    def inserir_elementos(self):
        ElementosBarra(self.estrutura).add_elementos(self.v, self.set_loc())
    
    def inserir_apoios(self):
        ins_apoios = ApoiosBarra(self.estrutura)
        ins_apoios.add_apoio(self.v, ins_apoios.nos_apoios(self.v))

    def momento_ext(self):

        carregametos = self.comb.CF, self.comb.CQP, self.comb.ATO
        names = ("CF", "CQP", "ATO")

        if self.comb.carregamento["permanente"] == 0.0 and self.comb.carregamento["acidental"] == 0.0:

            self._dict["CF"]  = [0.0 for i in self.v.node_map]
            self._dict["CQP"] = [0.0 for i in self.v.node_map]

            if not self.not_pp:
                self.setter_q_ext([-self.comb.ATO], ["ATO"])
            else: self._dict["ATO"] = [0.0 for i in self.v.node_map]
        
        else:
            carregametos = -self.comb.CF, -self.comb.CQP, -self.comb.ATO
            names = ("CF", "CQP", "ATO")
            self.setter_q_ext(carregametos, names)
            

    def setter_q_ext(self, values, names = None):

        #values = -self.comb.CF, -self.comb.CQP, -self.comb.ATO
        
        num_nos = len(self.v.node_map)

        for q, name in zip(values, names):
            for id_elem in range(1,num_nos):
                self.v.q_load(q = q, element_id= id_elem)

            self.solve()
            #self.v.show_bending_moment()
            self._dict[name] = self.get_momentos()
            

    def get_momentos(self):
        tmp_m = self.v.get_element_results(element_id=0, verbose= True)
        Momento = [-i["M"][0] for i in tmp_m]
        Momento.append(-tmp_m[-1]["M"][-1])
        return Momento

    def solve(self):
        self.v.solve()
    
    def _add_momentos(self):
        self.inserir_elementos()
        self.inserir_apoios()
        self.momento_ext()

    @property
    def CF(self): return self._dict["CF"]
    @property
    def CQP(self): return self._dict["CQP"]
    @property
    def ATO(self): return self._dict["ATO"]

def particionamento(xi, xf, part= 1):
    #xf += part
    p = np.round(np.arange(xi,xf, part),3)
    #print(p)
    return list(p)

if __name__ == "__main__":

    print(particionamento(0.0,16.0, 0.66666667))
    # t = [["retilineo",[[0.0, 0.08], [8, 0.08]]],
    #     ["retilineo",[[8, 0.08], [16, 0.08]]]]
    # f = {   
    #     "type" : "discreto",
    #         "x" : [0,1,2,3,4,5,6,7,8,9,10, 11,12, 13,14, 15,16],

    #             "f0" :[14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
    #             , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9],

    #         "finf": [14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
    #         , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9]}
    # est = {
    # "nos" : {"1": 0.0, "2": 8.0, "3": 16.0},
    # "elementos" : {"1": ["1", "2"], "2" : ["2","3"]},
    # "apoios" : {"1": "hinged", "2" : "roll", "3" : "roll"}}
    # carregamento ={
    # "permanente" : 0.0, 
    # "acidental" : 0.0,
    # "tipo" : "residencial",
    # "peso_proprio" : 0.25
    # }

    # mh = MomentoHiperestatico(t, f, est, .25)
    # mh.v.show_structure()
    # #print(mh._dict)
    # # me = MomentoExterno(est,carregamento)
    # # #print(me._dict)
    # # me.v.show_structure()
    



    




