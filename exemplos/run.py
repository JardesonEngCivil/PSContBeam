
from software.Forca_nodais.Cargas_nodais import Gauss
from software.Armadura_ativa.Tracado import TracadoCabo
from software.Armadura_ativa.Forca import ForcaProtensao
import numpy as np
from anastruct import SystemElements

inf = {"elemento" : {"1": {"nos": [0,10], "E": 25e3, "A": 0.9, "I":0.16875, "wi": 0.225, "ws":-0.225,
                "tracado": [["retilineo", [[0.0, 0.75],[2.35, 0.75]], 0.75],
                            ["curvo_inflexao", [[2.35, 0.75],[5.96, 0.08]], 0.75, 0.5],
                            ["curvo_inflexao", [[5.96, 0.08],[10.0, 1.28]], 0.75, 0.5]]},
        "2": {"nos": [10,20], "E": 25e3, "A": 0.9, "I":0.16875, "wi": 0.225, "ws":-0.225,
                "tracado": [["curvo_inflexao", [[10.0, 1.28],[15.0, 0.16]], 0.75, 0.5],
                            ["curvo_inflexao", [[15.0, 0.16],[20.0, 1.28]], 0.75, 0.5]]},
        "3": {"nos": [20,30], "E": 25e3, "A": 0.9, "I":0.16875, "wi": 0.225, "ws":-0.225,
                "tracado": [["curvo_inflexao", [[20.0, 1.28],[24.04, 0.08]], 0.75, 0.5],
                            ["curvo_inflexao", [[24.04, 0.08],[27.65, 0.75]], 0.75, 0.5],
                            ["retilineo", [[27.65, 0.75],[30.0, 0.75]], 0.75]]}
                            },
        "apoio": [[0.0,"S_genero"], [10.0,"P_genero" ], [20.0,"P_genero" ], [30.0,"P_genero" ]]

}

f = { 
        "x" : [0,	0.833,	1.667,	2.5,	3.333,	4.167,	5,	5.833,	6.667,	7.5,	8.333,
        	9.167,	10,	10.833,	11.667,	12.5,	13.333,	14.167,	15,	15.833,	16.667,	17.5,
            	18.333,	19.167,	20,	20.833,	21.667,	22.5,	23.333,	24.167,	25,	25.833,	26.667,
                27.5,	28.333,	29.167,	30],

            "f_0" :[97.66,	97.52,	97.22,	95.41,	93.76,	92.58,	90.47,	86.78,	82.92,	
            78.7,	74.77,	71.04,	68.14,	65.56,	63.75,	62.16,	60.26, 58.31,	56.47,
            	54.74,	53.22,	51.72,	50.4,	48.96,	47.24,	45.23,	43.06,	40.83,	38.58,
                	36.85,	35.47,	34.78,	34.33,	33.7,	33.07,	32.95,	32.9],

        "f_inf": [90.98, 90.88, 90.65,	89.26, 87.99, 87.11, 85.55,	82.76, 79.75, 76.41, 73.28,
        70.26, 67.87, 65.56, 63.75,	62.16, 60.26, 58.31, 56.47,	54.74, 53.22, 51.72, 50.4,
        48.96, 47.24, 45.23, 43.06, 40.83, 38.58, 36.85, 35.47,	34.78, 34.33, 33.7,	33.07, 32.95,32.9
    ]
        

    }

parabola =  {
    "elemento": {"1": {"nos": [0,8], "E": 25, "A": 0.1, "I":0.002083, "wi": 0.008333, "ws":-0.008333,
                       "tracado": [["curvo", [[0.0, 0.25], [4, 0.08]], 0.25],
                                    ["curvo", [[4, 0.08], [8, 0.25]], 0.25]]},
                 "2": {"nos": [8,16], "E": 25, "A": 0.1, "I":0.002083, "wi": 0.008333, "ws":-0.008333,
                       "tracado": [["curvo", [[8, 0.25], [12, 0.08]], 0.25],
                                    ["curvo",[[12, 0.08], [16, 0.25]], 0.25]]}},
    "apoio": [[0.0,"S_genero"], [8.0,"P_genero" ], [16.0,"P_genero" ]]
}

f1 = { 
        "x" : [0,1,2,3,4,5,6,7,8,9,10, 11,12, 13,14, 15,16],

            "f_0" :[14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
            , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9],

        "f_inf": [14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
        , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9]
    }


#print(estrutura["elemento"]["1"]["tracado"])


#print(parabola)

class Momento:


    def  __init__(self, elemento, f):
        
        self.elemento = elemento
        self.f = ForcaProtensao(f)
        self.t = TracadoCabo()

        self.m = []
        self.e = []
        self.x = []

        self.setter_momento()

    def _area_ret(self,coords, y):

        i = [coords[0][0], coords[1][0]]
        area_ret = Gauss().quadratura_gauss(self.t.retilineo, i, coords, y)
        
        self.set_e_x(i,self.t.retilineo, coords, y)
        return area_ret

    def _area_curva(self,coords, y):

        i = [coords[0][0], coords[1][0]]
        area_curva = Gauss().quadratura_gauss(self.t.curva, i, coords, y)

        self.set_e_x(i,self.t.curva, coords, y)
        return area_curva

    def _area_inf(self, coords, y, k):
        
        i = [coords[0][0], coords[1][0]]
        xp = (coords[1][0] - coords[0][0])
        xi = k*xp + coords[0][0]
    
        limite1 = [coords[0][0], xi]
        limite2 = [xi, coords[1][0]]

        area_inflexao =  Gauss().quadratura_gauss(self.t.inflexão, limite1, coords, y, k)
        area_inflexao += Gauss().quadratura_gauss(self.t.inflexão, limite2, coords,y , k)

        self.set_e_x(i, self.t.inflexão, coords, y, k)
        print(area_inflexao)
        return area_inflexao

    def momento_pont(self, area, l):
        #x = l[]
        momento = -round(self.f.f(l/2)*area/l,4)

        if bool(self.m) is False:
                self.m.append(momento)
                self.m.append(momento)
                 
        else:
            self.m[-1]-= momento
            self.m.append(momento)


    def set_e_x(self, t, func, coords, y, k= None):

        part = list(np.linspace(t[0], t[1], num = 5))

        for i in part:
            self.e.append(func(coords, i, y, k))
            self.x.append(i)
            

    def setter_momento(self):
        for i in self.elemento:
            l = self.elemento[i]["nos"][1] - self.elemento[i]["nos"][0]
            area = 0
            for k in self.elemento[i]["tracado"]:
                if k[0] == "retilineo":
                    area += self._area_ret(k[1], k[2])

                if k[0] == "curvo":
                    area += self._area_curva(k[1], k[2])

                if k[0] == "curvo_inflexao":
                    area += self._area_inf(k[1], k[2], k[3])

            self.momento_pont(area, l)
            

#t = Momento(inf["elemento"], f)
#print(t.m)
#print(t._area_ret(estrutura["elemento"]["1"]["tracado"][0][1], .25))

      
#m = [1.6887, 0.0, 1.6887]
m =[-12.7653, -10.1988, 10.1988, -12.7653]

viga = SystemElements()
viga.add_element(location=[[0,0],[10,0]])
viga.add_element(location=[[10,0],[20,0]])
viga.add_element(location=[[20,0],[30,0]])

viga.add_support_hinged(node_id= 1)
# viga.add_support_roll(node_id= 2)
# viga.add_support_roll(node_id= 3)
viga.add_support_roll(node_id= 4)

# c = 1
# for i in m:
#     viga.moment_load(node_id= c, Ty= i)
#     c+=1
viga.point_load(node_id= 2,Fy = -1.43)
viga.point_load(node_id= 3,Fy = .33)
#viga.show_structure()
viga.solve()
#viga.show_reaction_force()

#v = viga.get_element_results(element_id=0, verbose= True)
#print(v[0]["M"])
viga.show_bending_moment()
