from PSContBeam.momentos.viga import ElementosBarra, ApoiosBarra
from PSContBeam.forcasnodais.cargasnodais import MomentosNodais
from anastruct import SystemElements

class Reacao(dict):

    def __init__(self, tracado,force, estrutura, cg,  size = 1):
        self.estrutura = estrutura
        self.mn = MomentosNodais(tracado, force,cg,size) 
        self.v = SystemElements(mesh= 5)

        self._add_reaction()

    def inserir_elementos(self):
        ElementosBarra(self.estrutura).add_elementos(self.v, self.mn["x"])

    def inserir_apoios(self):
        ins_apoios = ApoiosBarra(self.estrutura)
        ins_apoios.add_apoio(self.v, ins_apoios.nos_apoios(self.v))

    def get_nos_m(self):
        nos = [[x, 0] for x in self.mn["x"]]
        nos_m = [self.v.find_node_id(no) for no in nos]
        return nos_m

    def inserir_momentos_nodais(self):
        typ = ["m", "m0"]
        for i in typ:
            for no_id, ty in zip(self.get_nos_m(), self.mn[i]):
                self.v.moment_load(node_id= no_id, Ty= ty)
           # self.v.show_structure()
            self.get_reacoes(i)

    def get_reacoes(self, typ):
        r = []
        self.v.solve()
        #self.v.show_reaction_force()
        for i in list(self.v.reaction_forces.values())[1:-1]:
            r.append([i.vertex.x, i.Fy])

        self[typ] = r

    def _add_reaction(self):
        self.inserir_elementos()
        self.inserir_apoios()
        self.inserir_momentos_nodais()

if __name__ == "__main__":
    t = [["retilineo",[[0.0, 0.08], [8, 0.08]], 0.25],
        ["retilineo",[[8, 0.08], [16, 0.08]], 0.25]]
    f = {   
        "type" : "discreto",
            "x" : [0,1,2,3,4,5,6,7,8,9,10, 11,12, 13,14, 15,16],

                "f0" :[14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
                , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9],

            "finf": [14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9
            , 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9, 14.9]}
    est = {
    "nos" : {"1": 0.0, "2": 8.0, "3": 16.0},
    "elementos" : {"1": ["1", "2"], "2" : ["2","3"]},
    "apoios" : {"1": "hinged", "2" : "roll", "3" : "roll"}}



    r = Reacao(t, f, est)
    r.v.show_structure()
    print(r)
