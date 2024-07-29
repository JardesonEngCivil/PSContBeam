from PSContBeam.Tensao.Tensoes import Tensao
from PSContBeam.Executor.leitura_arq import  leitura_dados


dados = leitura_dados("ex.json")

tensao = Tensao(dados, size= 1, part= .5)
tensao.plot_f()
tensao.plot_momento_hiperestatico()
tensao.plot_els_f()
tensao.plot_els_d()
tensao.plot_elu_ato()


