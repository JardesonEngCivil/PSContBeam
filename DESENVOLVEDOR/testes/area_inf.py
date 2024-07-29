from PSContBeam.protensao.functracado import ParabolaInflexao
from PSContBeam.forcasnodais.cargasnodais import Gauss
from sympy import integrate, Symbol


inf = [[5.96, 0.08],[10.0, 1.28]]
k = .5
cg = 0.75

func = ParabolaInflexao(inf, cg, k)
xi = 7.98
area1 = Gauss()._area(func, 5.96, 10)
area2 = Gauss()._area(func, xi, 10)
area = area1 + area2
#area = inf[0][1]*inf[1][0] - area
print(area1)

x = Symbol("x")
f1 = cg - (0.14704440741103814*(x - 5.96)**2 + 0.08)
f2 = cg - (-0.14704440741103814*(10 - x)**2 + 1.28)


a1 = integrate(f1, (x, 5.96, xi)).evalf()
a2 = integrate(f2, (x, xi, 10)).evalf()
a12 = a1 + a2
print(a12)