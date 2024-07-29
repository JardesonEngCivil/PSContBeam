from PSContBeam.Tensao.Tensoes import Tensao
from PSContBeam.Executor.leitura_arq import  leitura_dados
from PSContBeam.DESENVOLVEDOR.planilha import criar_resultados_xlsx, get_parms
from PSContBeam.exemplos.tensoes_vpro import inflexao
#import numpy as np



dados = leitura_dados("inflexao.json")

tensao = Tensao(dados, size=.5, not_pp= False, part= .833333)
#tensao.plot_momento_hiperestatico()

#get_parms(tensao.m_ext["ATO"], "ms-ATO", __file__)
#criar_resultados_xlsx(tensao.elu_ato().inf(), tensao.elu_ato().sup(), __file__, "ELU_ATO")


tensao.plot_f()
tensao.plot_momento_hiperestatico()
tensao.plot_els_f(inf= inflexao["els-f"][1], sup = inflexao["els-f"][0])
tensao.plot_els_d(inf= inflexao["els-d"][1], sup = inflexao["els-d"][0])
tensao.plot_elu_ato(inf= inflexao["elu-ato"][1], sup = inflexao["elu-ato"][0])










# tensao.plot_els_f(inf = inflexao["els-f"][1],
#                   sup = inflexao["els-f"][0])
# tensao.plot_els_d(inf = inflexao["els-d"][1],
#                   sup = inflexao["els-d"][0])
# tensao.plot_elu_ato(inf = inflexao["elu-ato"][1],
#                   sup = inflexao["elu-ato"][0])

