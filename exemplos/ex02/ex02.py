from PSContBeam.Tensao.Tensoes import Tensao
from PSContBeam.Executor.leitura_arq import  leitura_dados
from PSContBeam.DESENVOLVEDOR.planilha import criar_resultados_xlsx
from PSContBeam.exemplos.tensoes_vpro import curva
import numpy as np



dados = leitura_dados("parabola.json")

tensao = Tensao(dados, size=.5, not_pp= True, part = 0.6666667)
#print(tensao.e)
tensao.plot_momento_hiperestatico()
#criar_resultados_xlsx(tensao.elu_ato().inf(), tensao.elu_ato().sup(), __file__, "ELU-ATO")

# tensao.plot_els_f(inf = curva["els-f"][1],
#                   sup = curva["els-f"][0])
# tensao.plot_els_d(inf = curva["els-d"][1],
#                   sup = curva["els-d"][0])
# tensao.plot_elu_ato(inf = curva["elu-ato"][1],
#                   sup = curva["elu-ato"][0])


array = np.array([-2, -1, 1, 2], dtype= float)
array2 = np.array([-2, -1, 1, 2], dtype= float)
# array = np.where(array < 0, array - 2, array)
# print(array)
for i in range(len(array)):
            if array[i] < 0:
                array2[i] = array2[i] - 2
            else:
                array2[i] = array[i] / 2
print(array2)