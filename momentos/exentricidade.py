from PSContBeam.protensao.functracado import TracadoFactory
from PSContBeam.momentos.momentos import particionamento
import numpy as np

class Exentricidade(list):

    def __init__(self, tracado, cg, part = 1) -> None:
        self.tracado = TracadoFactory(tracado, cg)
        self.part  = part
        self.__append_values()
        #self.set_e()
    @property
    def set_pos(self):
        xi = self.tracado[0].x0
        xf = self.tracado[-1].xf
        return particionamento(xi,xf, self.part)

    def __append_values(self):

        c = 0
        xi = -1
        for j in self.set_pos:
            if j> xi and j<= self.tracado[c].xf:
                self.append(self.tracado[c].t(j))  
            else:
                xi = self.tracado[c].xf
                c += 1
                self.append(self.tracado[c].t(j))

    def set_e(self):
        for i in self.set_pos:
            for j in self.tracado:
                if i < j.xf:
                    self.append(j.t(i))
                    break


if __name__ == "__main__":
    t = [["retilineo",[[0.0, 0.08], [8, 0.08]]],
        ["retilineo",[[8, 0.08], [16, 0.08]]]]
        
    e = Exentricidade(t,.25)
    print(e)