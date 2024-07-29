from abc import ABC, abstractmethod

#Simple Factory
class Tracado(ABC):

    @abstractmethod
    def t_ordenada(): pass

    @abstractmethod
    def t(): pass

class Retilineo(Tracado):

    def __init__(self, loc, cg) -> None:
        
        self.loc, self.cg = loc, cg

        self.x0 = self.loc[0][0]
        self.y0 = self.loc[0][1]
        self.xf = self.loc[1][0]
        self.yf = self.loc[1][1]

    def t_ordenada(self, pos):
        
        x = pos - self.x0
        a = (self.yf - self.y0)/(self.xf - self.x0)
        f = a*x + self.y0
        return f
    
    def t(self, pos):
        return self.cg - self.t_ordenada(pos)
    
class ParabolaSimples(Tracado):

    def __init__(self, loc, cg) -> None:

        self.loc, self.cg = loc, cg

        self.x0 = self.loc[0][0]
        self.y0 = self.loc[0][1]
        self.xf = self.loc[1][0]
        self.yf = self.loc[1][1]


    def t_ordenada(self, pos):
        
        
        if self.yf <= self.y0:
            x  = pos - self.x0
            a = (self.y0 - self.yf)/(self.x0 - self.xf)**2
            b = -2*a*(self.xf - self.x0)
            f = a*x**2 + b*x + self.y0
            return f
        
        else:
            x = self.x0 - pos 
            a = (self.yf - self.y0)/(self.xf - self.x0)**2
            f = a*x**2 + self.y0
            return f
    
    def t(self, pos):
        return self.cg - self.t_ordenada(pos)

class ParabolaInflexao(Tracado):
    def __init__(self, loc, cg, k) -> None:

        self.loc, self.cg, self.k = loc, cg, k
        self.x0 = self.loc[0][0]
        self.y0 = self.loc[0][1]
        self.xf = self.loc[1][0]
        self.yf = self.loc[1][1]
        self.xp = self.xf - self.x0
        self.xi = self.k*self.xp

    def t_ordenada(self, pos):

        if pos >= self.x0 and pos-self.x0 <= self.xi:
            x = pos - self.x0     
            a = -(self.y0 - self.yf)/(self.k*self.xp**2)
            #print(a, self.y0)
            f = a*x**2 + self.y0
            return f
        
        else:
            x = self.xf - pos
            a = -(self.y0 - self.yf)/((self.k - 1)*self.xp**2)
            #print(a, self.yf)
            f = a*x**2 + self.yf
            return f
        
    
    def t(self, pos):
        return self.cg - self.t_ordenada(pos)


class TracadoFactory(list):

    def __init__(self, tracado, cg):
        self._tracado = tracado
        self.cg = cg

        self.tracado()

    def tracado(self):
        for t in self._tracado:
            tipo = t[0]
            if tipo == "retilineo":
                self.append(Retilineo(t[1], self.cg))        
            if tipo == "parabola":
                self.append(ParabolaSimples(t[1], self.cg))
            if tipo == "parabolainflexao":
                self.append(ParabolaInflexao(t[1], self.cg, t[2]))
           # assert 0, f'{tipo} não é uma função existente no traçado'


if __name__ == "__main__":

    r = [[0., 0.], [5., .5]]
    cg = .25

    ret = Retilineo(r,cg)
    print(ret.t_ordenada(5.))