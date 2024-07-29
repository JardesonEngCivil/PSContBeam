from abc import ABC, abstractmethod
from sympy import symbols, lambdify

class Force(ABC):

    @abstractmethod
    def f0(): pass

    @abstractmethod
    def finf(): pass

class ForceFunc(Force):

    def __init__(self,exprf0, exprfinf):
        self._f0 = lambdify('x', exprf0)
        self._finf = lambdify('x', exprfinf)

    def f0(self, pos):
        return self._f0(pos)

    def finf(self, pos):
        return self._finf(pos)
    
class ForceDiscretize(Force):

    def __init__(self, x, discf0, discfinf):
        self.x = x
        self._f0 = discf0
        self._finf = discfinf

    def f0(self, pos):
        return self._set_f(pos, self._f0)

    def finf(self, pos):
        return self._set_f(pos, self._finf)

    def _set_f(self, pos,fd):
        for i in range(len(self.x)-1):
            if  pos >= self.x[i] and pos <= self.x[i+1]:
                f  = fd[i] + ((pos - self.x[i])*(fd[i+1]-fd[i])/(self.x[i+1]-self.x[i]))
                break
        return f

class ForceFactory:

    def __init__(self, forceProt):
        self._forceProt = forceProt


    def force(self) -> Force:
        tipo = self._forceProt["type"]

        if tipo == "discreto":  
            x = self._forceProt["x"]
            discf0 = self._forceProt["f0"]
            discfinf = self._forceProt["finf"]
            return ForceDiscretize(x, discf0, discfinf)
        
        if tipo == "funçao":
            exprf0 = self._forceProt["f0"]
            exprfinf = self._forceProt["finf"]
            return ForceFunc(exprf0, exprfinf)
        
        assert 0, "tipo de força não encontrado"


if __name__ == "__main__":
    fProt = {
        "type": "funçao",
        "x"   : "1, 10",
        "f0"  : "2*exp(x)",
        "finf": "3*exp(x)"
    }
    fProtd = {
        "type": "discreto",
        "x"   : [0, 5, 10],
        "f0"  : [2,10,20],
        "finf": [1,5,10]
    }
